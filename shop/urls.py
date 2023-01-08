from django.urls import path

from shop.api import ProductViewSet, CategoryViewSet

urlpatterns = [
    path('products/', ProductViewSet.as_view({
        'get': 'list'
    })),
    path('product/<int:pk>/', ProductViewSet.as_view({
        'get': 'retrieve'
    })),
    path('product/', ProductViewSet.as_view({
        'post': 'create'
    })),
    path('product/delete/<int:pk>/', ProductViewSet.as_view({
        'delete': 'destroy'
    })),
    path('product/update/<int:pk>/', ProductViewSet.as_view({
        'put': 'update',
        'patch': 'partial_update'
    })),
    path('categories/', CategoryViewSet.as_view({
        'get': 'list'
    })),
    path('category/<int:pk>/', CategoryViewSet.as_view({
        'get': 'retrieve'
    })),
    path('category/', CategoryViewSet.as_view({
        'post': 'create'
    })),
]
