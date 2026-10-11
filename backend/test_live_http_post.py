import urllib.request
import json

payload = {
    "customer_name": "lokesh",
    "customer_email": "lokesh25@gmail.com",
    "customer_phone": "9876543210",
    "shipping_address": "no27b,voc street , mgr nagar",
    "items": [
        {
            "product_id": 1,
            "product_name": "Turmeric Powder",
            "quantity": 1,
            "price": 5.0
        }
    ]
}

data = json.dumps(payload).encode('utf-8')
req = urllib.request.Request(
    "http://127.0.0.1:8000/api/orders/",
    data=data,
    headers={"Content-Type": "application/json"}
)

try:
    with urllib.request.urlopen(req) as response:
        status_code = response.getcode()
        body = response.read().decode('utf-8')
        print(f"STATUS: {status_code}")
        print("RESPONSE:", body)
except urllib.error.HTTPError as e:
    print(f"HTTP ERROR: {e.code}")
    print("ERROR BODY:", e.read().decode('utf-8'))
except Exception as e:
    print("ERROR:", str(e))
