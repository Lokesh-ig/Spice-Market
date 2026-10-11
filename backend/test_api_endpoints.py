import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from django.test import Client
from api.models import Product, Order, OrderItem, ContactMessage
from django.contrib.auth.models import User

def run_tests():
    client = Client()
    print("=" * 60)
    print("RUNNING SPICE MARKET API INTEGRATION TESTS")
    print("=" * 60)

    # 1. Health check
    res = client.get('/api/health/')
    assert res.status_code == 200, f"Health check failed: {res.status_code}"
    print("✅ 1. GET /api/health/ -> 200 OK:", res.json())

    # 2. Products List
    res = client.get('/api/products/')
    assert res.status_code == 200, f"Product list failed: {res.status_code}"
    products = res.json()
    assert len(products) >= 9, f"Expected at least 9 products, got {len(products)}"
    print(f"✅ 2. GET /api/products/ -> 200 OK (Loaded {len(products)} products)")

    # 3. Product Detail
    prod_id = products[0]['id']
    res = client.get(f'/api/products/{prod_id}/')
    assert res.status_code == 200, f"Product detail failed: {res.status_code}"
    print(f"✅ 3. GET /api/products/{prod_id}/ -> 200 OK ({res.json()['name']})")

    # 4. User Registration
    test_email = "testspiceuser@example.com"
    User.objects.filter(email=test_email).delete() # clean if exists
    reg_payload = {
        "name": "Spice Explorer",
        "email": test_email,
        "password": "SecretPassword123!",
        "phone": "9876543210"
    }
    res = client.post('/api/auth/register/', data=json.dumps(reg_payload), content_type='application/json')
    assert res.status_code == 201, f"Registration failed: {res.status_code} - {res.content}"
    print("✅ 4. POST /api/auth/register/ -> 201 Created:", res.json()['user']['email'])

    # 5. User Login
    login_payload = {
        "username_or_email": test_email,
        "password": "SecretPassword123!"
    }
    res = client.post('/api/auth/login/', data=json.dumps(login_payload), content_type='application/json')
    assert res.status_code == 200, f"Login failed: {res.status_code} - {res.content}"
    print("✅ 5. POST /api/auth/login/ -> 200 OK:", res.json()['user']['first_name'])

    # 6. Auth /me
    res = client.get('/api/auth/me/')
    assert res.status_code == 200, f"Auth me failed: {res.status_code}"
    print("✅ 6. GET /api/auth/me/ -> 200 OK:", res.json()['user']['username'])

    # 6b. Unauthenticated Order Rejected (Amazon/Flipkart gate)
    guest_client = Client()
    guest_order = {
        "customer_name": "Unregistered Guest",
        "customer_email": "stranger_guest@unknown.com",
        "shipping_address": "Unknown Road",
        "items": [{"product_id": products[0]['id'], "name": products[0]['name'], "quantity": 1, "price": 5}]
    }
    guest_res = guest_client.post('/api/orders/', data=json.dumps(guest_order), content_type='application/json')
    assert guest_res.status_code == 401, f"Expected 401 for guest order, got {guest_res.status_code}"
    print("✅ 6b. POST /api/orders/ without login -> 401 Unauthorized (Blocked unauthenticated checkout)")

    # 7. Create Order (Checkout with authenticated user)
    order_payload = {
        "customer_name": "Spice Explorer",
        "customer_email": test_email,
        "customer_phone": "9876543210",
        "shipping_address": "123 Cardamom Lane, Kochi, Kerala",
        "items": [
            {
                "product_id": products[0]['id'],
                "product_name": products[0]['name'],
                "quantity": 2,
                "price": float(products[0]['price'])
            },
            {
                "product_id": products[1]['id'],
                "product_name": products[1]['name'],
                "quantity": 1,
                "price": float(products[1]['price'])
            }
        ]
    }
    res = client.post('/api/orders/', data=json.dumps(order_payload), content_type='application/json')
    assert res.status_code == 201, f"Order creation failed: {res.status_code} - {res.content}"
    order_data = res.json()
    order_id = order_data['order']['id']
    total_amount = float(order_data['order']['total_amount'])
    expected_total = (2 * float(products[0]['price'])) + (1 * float(products[1]['price']))
    assert abs(total_amount - expected_total) < 0.01, f"Total mismatch: {total_amount} != {expected_total}"
    print(f"✅ 7. POST /api/orders/ -> 201 Created (Order #{order_id}, Total: ₹{total_amount:.2f})")

    # 8. List Orders
    res = client.get('/api/orders/')
    assert res.status_code == 200, f"Order list failed: {res.status_code}"
    assert len(res.json()) >= 1, "Expected at least 1 order in list"
    print(f"✅ 8. GET /api/orders/ -> 200 OK (Found {len(res.json())} orders)")

    # 9. Contact Message
    contact_payload = {
        "name": "Spice Lover",
        "email": "lover@spice.org",
        "message": "Do you offer wholesale bulk export for organic cinnamon?"
    }
    res = client.post('/api/contact/', data=json.dumps(contact_payload), content_type='application/json')
    assert res.status_code == 201, f"Contact message failed: {res.status_code} - {res.content}"
    print("✅ 9. POST /api/contact/ -> 201 Created:", res.json()['message'])

    # 10. Frontend page serving
    res = client.get('/')
    assert res.status_code == 200, f"Frontend home failed: {res.status_code}"
    body = b"".join(res.streaming_content) if hasattr(res, 'streaming_content') else res.content
    assert b"SPICE MARKET" in body, "index.html missing brand name"
    print("✅ 10. GET / -> 200 OK (Serves index.html with live backend integration)")

    res = client.get('/cart.html')
    assert res.status_code == 200, f"Frontend cart failed: {res.status_code}"
    body = b"".join(res.streaming_content) if hasattr(res, 'streaming_content') else res.content
    assert b"Your Spice Cart" in body, "Cart.html missing heading"
    print("✅ 11. GET /cart.html -> 200 OK (Serves Cart.html)")

    res = client.get('/signup.html')
    assert res.status_code == 200, f"Frontend signup failed: {res.status_code}"
    body = b"".join(res.streaming_content) if hasattr(res, 'streaming_content') else res.content
    assert b"Spice Market Family" in body, "signup.html missing title"
    print("✅ 12. GET /signup.html -> 200 OK (Serves signup.html)")

    print("=" * 60)
    print("🎉 ALL 12 INTEGRATION TESTS PASSED SUCCESSFULLY!")
    print("=" * 60)

if __name__ == '__main__':
    run_tests()
