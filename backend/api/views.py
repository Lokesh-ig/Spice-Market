from django.db import transaction, connection
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from api.authentication import CsrfExemptSessionAuthentication
from api.models import Product, Order, OrderItem, CartItem, ContactMessage
from api.serializers import (
    ProductSerializer, UserSerializer, RegisterSerializer,
    LoginSerializer, OrderSerializer, CartItemSerializer, ContactMessageSerializer
)


class HealthCheckView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        db_status = "ok"
        db_vendor = connection.vendor
        error_msg = None
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
        except Exception as e:
            db_status = "error"
            error_msg = str(e)

        return Response({
            "status": "online",
            "database": {
                "engine": db_vendor,
                "status": db_status,
                "error": error_msg
            },
            "product_count": Product.objects.count() if db_status == "ok" else 0
        })


class ProductListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        category = request.query_params.get('category')
        search = request.query_params.get('search')
        products = Product.objects.filter(is_active=True)

        if category:
            products = products.filter(category__iexact=category)
        if search:
            products = products.filter(name__icontains=search)

        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class ProductDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        try:
            product = Product.objects.get(pk=pk, is_active=True)
            return Response(ProductSerializer(product).data)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)


@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [CsrfExemptSessionAuthentication]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            login(request, user)
            return Response({
                "message": "Registration successful!",
                "user": UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [CsrfExemptSessionAuthentication]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            return Response({
                "message": "Login successful!",
                "user": UserSerializer(user).data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name='dispatch')
class LogoutView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [CsrfExemptSessionAuthentication]

    def post(self, request):
        logout(request)
        return Response({"message": "Logged out successfully."})


class CurrentUserView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [CsrfExemptSessionAuthentication]

    def get(self, request):
        if request.user.is_authenticated:
            return Response({"authenticated": True, "user": UserSerializer(request.user).data})
        return Response({"authenticated": False, "user": None})


@method_decorator(csrf_exempt, name='dispatch')
class OrderCreateAndListView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [CsrfExemptSessionAuthentication]

    def get(self, request):
        if request.user.is_authenticated:
            orders = Order.objects.filter(user=request.user).order_by('-created_at')
        else:
            orders = Order.objects.all().order_by('-created_at')[:10]
        return Response(OrderSerializer(orders, many=True).data)

    def post(self, request):
        data = request.data
        customer_name = data.get('customer_name', '').strip()
        customer_email = data.get('customer_email', '').strip()
        customer_phone = data.get('customer_phone', '').strip()
        shipping_address = data.get('shipping_address', '').strip()
        items_data = data.get('items', [])

        if not customer_name or not customer_email or not shipping_address:
            return Response({
                "error": "customer_name, customer_email, and shipping_address are required."
            }, status=status.HTTP_400_BAD_REQUEST)

        # Amazon / Flipkart style checkout requirement: user must be logged in or registered
        user = request.user if request.user.is_authenticated else None
        if not user and customer_email:
            user = User.objects.filter(email__iexact=customer_email).first()

        if not user:
            return Response({
                "error": "Authentication required. Please log in or sign up before placing an order."
            }, status=status.HTTP_401_UNAUTHORIZED)

        if not items_data or not isinstance(items_data, list):
            return Response({
                "error": "Cart cannot be empty. Please include items in the order."
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                total_amount = 0
                processed_items = []
                import re

                for item in items_data:
                    product_id = item.get('product_id')
                    product_name = item.get('name') or item.get('product_name', 'Spice Item')
                    quantity = int(item.get('quantity', 1))
                    weight = item.get('weight', '1 kg')

                    # Parse weight in kg accurately
                    weight_kg = 1.0
                    try:
                        if 'weight_kg' in item and item['weight_kg'] is not None:
                            weight_kg = float(item['weight_kg'])
                        elif 'g' in str(weight).lower() and 'kg' not in str(weight).lower():
                            m = re.search(r'([\d.]+)', str(weight))
                            if m:
                                weight_kg = float(m.group(1)) / 1000.0
                        elif 'kg' in str(weight).lower():
                            m = re.search(r'([\d.]+)', str(weight))
                            if m:
                                weight_kg = float(m.group(1))
                    except (ValueError, TypeError):
                        weight_kg = 1.0

                    if weight_kg <= 0:
                        weight_kg = 1.0

                    price = float(item.get('price', 0))

                    if product_id:
                        try:
                            prod_obj = Product.objects.get(pk=int(product_id))
                            product_name = prod_obj.name
                            base_1kg_price = float(prod_obj.price)
                            calculated_price = round(base_1kg_price * weight_kg, 2)
                            price = calculated_price if calculated_price > 0 else (price or base_1kg_price)
                        except (Product.DoesNotExist, ValueError, TypeError):
                            pass

                    # Ensure display name reflects chosen weight variant
                    if weight and f"({weight})" not in product_name:
                        full_display_name = f"{product_name} ({weight})"
                    else:
                        full_display_name = product_name

                    subtotal = round(price * quantity, 2)
                    total_amount += subtotal

                    processed_items.append({
                        "product_id": product_id,
                        "product_name": full_display_name,
                        "quantity": quantity,
                        "weight": str(weight),
                        "weight_kg": round(weight_kg, 3),
                        "unit_price": round(price, 2),
                        "subtotal": subtotal
                    })

                order = Order.objects.create(
                    user=request.user if request.user.is_authenticated else None,
                    customer_name=customer_name,
                    customer_email=customer_email,
                    customer_phone=customer_phone,
                    shipping_address=shipping_address,
                    total_amount=round(total_amount, 2),
                    status='pending'
                )

                for p_item in processed_items:
                    prod_fk = None
                    if p_item['product_id']:
                        try:
                            prod_fk = Product.objects.filter(pk=int(p_item['product_id'])).first()
                        except (ValueError, TypeError):
                            pass

                    OrderItem.objects.create(
                        order=order,
                        product=prod_fk,
                        product_name=p_item['product_name'],
                        quantity=p_item['quantity'],
                        weight=p_item['weight'],
                        weight_kg=p_item['weight_kg'],
                        unit_price=p_item['unit_price'],
                        subtotal=p_item['subtotal']
                    )

                return Response({
                    "message": "Order placed successfully!",
                    "order_id": order.id,
                    "order": OrderSerializer(order).data
                }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": f"Failed to place order: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class OrderDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
            return Response(OrderSerializer(order).data)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)


@method_decorator(csrf_exempt, name='dispatch')
class CartView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [CsrfExemptSessionAuthentication]

    def get(self, request):
        if not request.user.is_authenticated:
            return Response({"items": [], "total": 0})
        items = CartItem.objects.filter(user=request.user).select_related('product')
        import re
        total = 0
        for item in items:
            w_str = str(item.weight).lower()
            w_kg = 1.0
            if 'g' in w_str and 'kg' not in w_str:
                m = re.search(r'([\d.]+)', w_str)
                if m:
                    w_kg = float(m.group(1)) / 1000.0
            elif 'kg' in w_str:
                m = re.search(r'([\d.]+)', w_str)
                if m:
                    w_kg = float(m.group(1))
            line_price = round(float(item.product.price) * w_kg, 2)
            total += round(line_price * item.quantity, 2)

        return Response({
            "items": CartItemSerializer(items, many=True).data,
            "total": round(total, 2)
        })

    def post(self, request):
        if not request.user.is_authenticated:
            return Response({"error": "Login required for persistent cart syncing"}, status=status.HTTP_401_UNAUTHORIZED)
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))
        weight = request.data.get('weight', '1 kg')

        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product, weight=weight)
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = max(1, quantity)
        cart_item.save()

        return Response(CartItemSerializer(cart_item).data, status=status.HTTP_200_OK)

    def delete(self, request):
        if not request.user.is_authenticated:
            return Response({"error": "Login required"}, status=status.HTTP_401_UNAUTHORIZED)
        item_id = request.data.get('item_id')
        if item_id:
            CartItem.objects.filter(user=request.user, id=item_id).delete()
        else:
            CartItem.objects.filter(user=request.user).delete()
        return Response({"message": "Cart updated"})


@method_decorator(csrf_exempt, name='dispatch')
class ContactMessageView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [CsrfExemptSessionAuthentication]

    def get(self, request):
        messages = ContactMessage.objects.all().order_by('-created_at')[:20]
        return Response(ContactMessageSerializer(messages, many=True).data)

    def post(self, request):
        serializer = ContactMessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Thank you! Your message has been received and saved.",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
