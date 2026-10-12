from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from api.models import Product, Order, OrderItem, CartItem, ContactMessage


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'image_url', 'category', 'stock', 'is_active', 'created_at']


class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined', 'avatar']

    def get_avatar(self, obj):
        if obj.email:
            return f"https://unavatar.io/{obj.email.strip().lower()}"
        return None


class RegisterSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=150, required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(min_length=6, write_only=True, required=True)
    phone = serializers.CharField(max_length=20, required=False, allow_blank=True, default='')

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("An account with this email already exists.")
        return value

    def create(self, validated_data):
        email = validated_data['email'].lower()
        # Use email or username derived from email
        username = email.split('@')[0]
        base_username = username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1

        user = User.objects.create_user(
            username=username,
            email=email,
            password=validated_data['password'],
            first_name=validated_data.get('name', '')
        )
        return user


class LoginSerializer(serializers.Serializer):
    username_or_email = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        ident = data.get('username_or_email', '').strip()
        pwd = data.get('password', '')

        user = None
        # Check if login with email
        if '@' in ident:
            try:
                user_obj = User.objects.get(email__iexact=ident)
                user = authenticate(username=user_obj.username, password=pwd)
            except User.DoesNotExist:
                user = None
        else:
            user = authenticate(username=ident, password=pwd)

        if not user:
            raise serializers.ValidationError("Invalid email/username or password.")
        if not user.is_active:
            raise serializers.ValidationError("This user account is inactive.")

        data['user'] = user
        return data


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'quantity', 'weight', 'weight_kg', 'unit_price', 'subtotal']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'user', 'customer_name', 'customer_email',
            'customer_phone', 'shipping_address', 'total_amount',
            'delivery_fee', 'total_weight_kg',
            'status', 'created_at', 'items'
        ]


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source='product', write_only=True
    )

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_id', 'quantity', 'weight', 'created_at']


class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ['id', 'name', 'email', 'message', 'status', 'created_at']
        read_only_fields = ['status', 'created_at']
