# 🌶️ Spice Market — Luxury Artisanal E-Commerce Platform

A premium, full-stack artisanal spice marketplace delivering single-origin organic spices with an authentic grocery shopping experience, real-time gram/kilogram price calculation, glassmorphic UI, and Django REST backend.

---

## ✨ Features

- **⚖️ Dynamic Weight & Price Calculation**: Base prices are calibrated for 1 kg, with interactive pack sizing (100g, 250g, 500g, 1 kg, 2 kg) plus custom gram/kilogram inputs that update line items and totals in real time.
- **🎨 Luxury Dark Glassmorphic Aesthetic**: Deep obsidian backgrounds, warm amber/saffron accents, glowing capsules, and smooth micro-interactions.
- **🛒 Dynamic Shopping Cart**:
  - Live in-cart pack size switcher
  - Real-time quantity steppers
  - Total spice net weight calculation in kilograms and grams
  - Custom non-blocking toast notifications and confirmation dialogs
- **🔐 User Authentication**: Amazon/Flipkart-style checkout gating, user session persistence, and order tracking.
- **⚡ RESTful Django Backend**:
  - Modular architecture with clean API endpoints (`/api/products/`, `/api/orders/`, `/api/auth/`, etc.)
  - Support for SQLite and MySQL with automatic graceful fallback
  - Weight variant tracking in database models and migrations

---

## 📁 Project Structure

```
├── Spicy market website/     # Frontend Client Application
│   ├── index.html            # Luxury Home & Product Showcase
│   ├── Cart.html             # Interactive Shopping Cart & Checkout
│   ├── signup.html           # Authentication & Account Portal
│   ├── style.css             # Glassmorphism & Responsive Styling
│   ├── api.js                # Frontend API Client Module
│   └── *.png, *.jpg          # High-resolution spice assets & favicons
├── backend/                  # Django REST API Backend
│   ├── api/                  # API models, serializers, views, migrations
│   ├── backend_project/      # Settings, ASGI/WSGI configuration
│   ├── manage.py             # Django management CLI
│   └── requirements.txt      # Python dependencies
└── .gitignore                # Production git ignore rules
```

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- Python 3.10+
- Modern Web Browser (Chrome, Edge, Firefox, Safari)

### 2. Backend Setup
```bash
# Navigate to backend directory
cd backend

# Create & activate virtual environment (optional)
python -m venv venv
# Windows:
.\venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Seed catalog products (15 single-origin spices)
python manage.py seed_data

# Start backend server
python manage.py runserver 8000
```

### 3. Frontend Access
Once the backend is running, open:
`http://127.0.0.1:8000/index.html` or open `Spicy market website/index.html` directly in your browser.

---

## 📜 License
Crafted with passion for culinary excellence. All rights reserved.
