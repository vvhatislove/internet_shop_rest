from rest_framework import serializers

from shop.models import Product, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ('slug',)


class ProductReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Product
        exclude = ('stock', 'available', 'created', 'updated')


class ProductEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ('created', 'updated')
        read_only_fields = ('slug',)
