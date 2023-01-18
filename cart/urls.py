from django.urls import path

from cart.api import CartViewSet

urlpatterns = [
    path('cart/', CartViewSet.as_view(
        {
            'get': 'list',
            'post': 'create',
            'delete': 'cart_clear'
        })),
    path('cart/item-cart/<int:pk>/', CartViewSet.as_view(
        {
            'get': 'retrieve',
            'delete': 'destroy',
            'put': 'update',
            'patch': 'update'
        }
    ))
]
