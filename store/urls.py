from django.urls import path
from .views import store_home, cart_add, cart_view, cart_remove, checkout, order_history, profile

urlpatterns = [
    path('', store_home, name='store'),
    path('cart/', cart_view, name='cart'),
    path('cart/add/<int:product_id>/', cart_add, name='cart_add'),
    path('cart/remove/<int:product_id>/', cart_remove, name='cart_remove'),
    path('checkout/', checkout, name='checkout'),
    path('orders/', order_history, name='order_history'),
    path('profile/', profile, name='profile'),
]
