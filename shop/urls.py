from django.urls import path

from shop.api import ProductViewSet, CategoryViewSet

urlpatterns = [
    path('products/', ProductViewSet.as_view({
        'get': 'list'
    })),
    path('product/<int:pk>/', ProductViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    })),
    path('product/', ProductViewSet.as_view({
        'post': 'create'
    })),
    path('categories/', CategoryViewSet.as_view({
        'get': 'list'
    })),
    path('category/<int:pk>/', CategoryViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    })),
    path('category/', CategoryViewSet.as_view({
        'post': 'create'
    })),
]
