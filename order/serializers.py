from rest_framework import serializers

from order.models import OrderItem, Customer


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        exclude = ('updated', 'created',)
        read_only_fields = ('user',)
