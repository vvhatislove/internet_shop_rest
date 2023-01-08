from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import permissions

from cart.models import CartItem
from cart.serializers import CartItemAddDeleteSerializer, CartItemReadSerializer, CartItemUpdateSerializer
from rest_framework.viewsets import ModelViewSet


class CartViewSet(ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemAddDeleteSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        total_sum = sum(item['total'] for item in serializer.data)
        response_data = {'cart': serializer.data, 'total_sum': total_sum}
        return Response(response_data)

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return CartItemReadSerializer
        elif self.action == 'update':
            return CartItemUpdateSerializer
        return self.serializer_class

    @action(detail=False, methods=['delete'])
    def cart_clear(self, request):
        cart_items = self.get_queryset().filter(cart__user=request.user)
        cart_items.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
