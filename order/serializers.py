from django.contrib.auth import get_user_model
from rest_framework import serializers

from order.models import OrderItem, Customer, Order

User = get_user_model()


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')


class CustomerSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)

    class Meta:
        model = Customer
        exclude = ('updated', 'created',)
        read_only_fields = ('user',)

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
