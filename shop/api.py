from django.db.models import QuerySet
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from shop.models import Product, Category
from shop.serializers import ProductReadSerializer, ProductEntrySerializer, CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductReadSerializer

    def list(self, request, *args, **kwargs):
        category_id = request.query_params.get('category_id')
        if category_id:
            try:
                category_id = int(category_id)
            except ValueError:
                return super().list(request, *args, **kwargs)
        else:
            return super().list(request, *args, **kwargs)
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(category__pk=category_id)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

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
