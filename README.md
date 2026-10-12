# 🌶️ Spice Market — Luxury Artisanal E-Commerce Platform

[![Live Website](https://img.shields.io/badge/Live_Website-spice--market.onrender.com-00d2ff?style=for-the-badge&logo=render&logoColor=white)](https://spice-market.onrender.com)
[![Database](https://img.shields.io/badge/Database-TiDB_Cloud_MySQL-0077ff?style=for-the-badge&logo=mysql&logoColor=white)](https://tidbcloud.com)
[![Backend](https://img.shields.io/badge/Backend-Django_5_REST_Framework-092E20?style=for-the-badge&logo=django&logoColor=white)](https://spice-market.onrender.com/api/health/)
[![Python](https://img.shields.io/badge/Python-3.10-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)

> 🌐 **Live Production Store**: **[https://spice-market.onrender.com](https://spice-market.onrender.com)**  
> ⚡ **Live API Health Check**: **[https://spice-market.onrender.com/api/health/](https://spice-market.onrender.com/api/health/)**  
> 📋 **Architecture Showcase**: **[`Spicy market website/showcase_card.html`](file:///Spicy%20market%20website/showcase_card.html)**

A premium, full-stack artisanal spice marketplace delivering single-origin organic spices with an authentic grocery shopping experience, real-time gram/kilogram price calculation, glassmorphic UI, and Django REST backend.

---

## ✨ Features

- **🚚 Weight-Based Delivery Fee Engine**:
  - Automatically calculates total order spice weight in kilograms and grams.
  - Applies standard courier delivery fee (**+₹50.00**) for orders **under 1 kg (`< 1000g`)**.
  - Unlocks **FREE Delivery (₹0.00)** for orders **1 kg or more (`>= 1000g`)**.
  - Features real-time Swiggy/Amazon-style progress nudge bar indicating remaining grams to unlock free dispatch.
- **⚖️ Dynamic Weight & Price Calculation**: Base prices are calibrated for 1 kg, with interactive pack sizing (100g, 250g, 500g, 1 kg, 2 kg) plus custom gram/kilogram inputs that update line items and totals in real time.
- **🎨 Luxury Dark Glassmorphic Aesthetic**: Deep obsidian backgrounds, warm amber/saffron accents, glowing capsules, and smooth micro-interactions.
- **🛒 Dynamic Shopping Cart**:
  - Live in-cart pack size switcher
  - Real-time quantity steppers
  - Total spice net weight calculation in kilograms and grams
  - Custom non-blocking toast notifications and confirmation dialogs
- **🔐 User Authentication**: Amazon/Flipkart-style checkout gating, user session persistence, Google OAuth avatar support, and order tracking.
- **⚡ RESTful Django Backend & TiDB Cloud MySQL**:
  - Modular architecture with clean API endpoints (`/api/products/`, `/api/orders/`, `/api/auth/`, etc.)
  - Powered by high-availability **TiDB Cloud Serverless MySQL** with TLS encryption.
  - Fully containerized with **Gunicorn** and **WhiteNoise** on **Render**.

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
