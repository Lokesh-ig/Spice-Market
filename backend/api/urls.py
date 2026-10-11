from django.urls import path
from api.views import (
    HealthCheckView, ProductListView, ProductDetailView,
    RegisterView, LoginView, LogoutView, CurrentUserView,
    OrderCreateAndListView, OrderDetailView, CartView, ContactMessageView
)

urlpatterns = [
    # Health & System
    path('health/', HealthCheckView.as_view(), name='health-check'),

    # Products
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),

    # Authentication
    path('auth/register/', RegisterView.as_view(), name='auth-register'),
    path('auth/login/', LoginView.as_view(), name='auth-login'),
    path('auth/logout/', LogoutView.as_view(), name='auth-logout'),
    path('auth/me/', CurrentUserView.as_view(), name='auth-current-user'),

    # Orders & Checkout
    path('orders/', OrderCreateAndListView.as_view(), name='order-list-create'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),

    # Persistent Cart
    path('cart/', CartView.as_view(), name='cart'),

    # Contact & Inquiries
    path('contact/', ContactMessageView.as_view(), name='contact-message'),
]
