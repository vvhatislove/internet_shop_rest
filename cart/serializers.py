from rest_framework import serializers

from cart.models import Cart, CartItem
from shop.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('name', 'image', 'vendor_code', 'price',)


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'


class CartItemAddDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ('id', 'quantity', 'product', 'cart')
        read_only_fields = ('cart', 'id')

    def create(self, validated_data):
        is_created = False
        try:
            cart = Cart.objects.get(user=self.context['request'].user)
        except Cart.DoesNotExist:
            cart = Cart.objects.create(user=self.context['request'].user)
            is_created = True
        validated_data['cart'] = cart
        if not is_created:
            item = cart.cartitem_set.filter(product_id=validated_data['product'].id)
            if len(item) == 1:
                item = item[0]
                validated_data['quantity'] += item.quantity
                return super().update(item, validated_data)
        return super().create(validated_data)


class CartItemReadSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    total = serializers.SerializerMethodField(method_name='get_total')

    class Meta:
        model = CartItem
        exclude = ('created', 'updated', 'cart')

    @staticmethod
    def get_total(instance):
        return instance.product.price * instance.quantity


class CartItemUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ('quantity',)
