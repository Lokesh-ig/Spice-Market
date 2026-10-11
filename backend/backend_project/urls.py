from pathlib import Path
from django.contrib import admin
from django.urls import path, include, re_path
from django.http import FileResponse, Http404
from django.conf import settings
from django.conf.urls.static import static

FRONTEND_DIR = Path(settings.BASE_DIR).parent / 'Spicy market website'

def serve_frontend_page(request, filename):
    file_path = FRONTEND_DIR / filename
    if file_path.exists() and file_path.is_file():
        return FileResponse(open(file_path, 'rb'))
    raise Http404("Page not found")

def home_view(request):
    return serve_frontend_page(request, 'index.html')

def cart_view(request):
    return serve_frontend_page(request, 'Cart.html')

def signup_view(request):
    return serve_frontend_page(request, 'signup.html')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),

    # Frontend Page Routes
    path('', home_view, name='home'),
    path('index.html', home_view, name='index-html'),
    path('cart/', cart_view, name='cart-page'),
    path('Cart.html', cart_view, name='cart-page-file'),
    path('cart.html', cart_view, name='cart-page-file-lower'),
    path('signup/', signup_view, name='signup-page'),
    path('signup.html', signup_view, name='signup-page-file'),
]

# Static files handling for frontend images and CSS
urlpatterns += static(settings.STATIC_URL, document_root=str(FRONTEND_DIR))

# Also allow direct asset access matching relative paths (e.g., img_1.png.png, style.css)
def serve_direct_asset(request, asset_name):
    file_path = FRONTEND_DIR / asset_name
    if file_path.exists() and file_path.is_file():
        return FileResponse(open(file_path, 'rb'))
    raise Http404("Asset not found")

urlpatterns += [
    re_path(r'^(?P<asset_name>[\w\-]+\.(?:png|jpg|jpeg|avif|css|js|ico|svg)(?:\.png)?)$', serve_direct_asset),
]
