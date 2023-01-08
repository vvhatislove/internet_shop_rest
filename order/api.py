from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import permissions

from order.models import Order, Customer
from order.serializers import CustomerSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def get_customer_info(self, request, *args, **kwargs):
        instance = self.get_queryset().get(user=request.user)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def create_order(self, request, *args, **kwargs):
        pass
