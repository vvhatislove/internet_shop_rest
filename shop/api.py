from rest_framework import permissions
from rest_framework import viewsets

from shop.models import Product, Category
from shop.serializers import ProductReadSerializer, ProductEntrySerializer, CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductReadSerializer

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return ProductEntrySerializer
        return self.serializer_class

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]
