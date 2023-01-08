from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import permissions

from order.models import Order, Customer
from order.serializers import CustomerSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    customer_does_not_exist_message = 'customer does not exist, please create one'

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_queryset().get(user=request.user)
        except Customer.DoesNotExist:
            return Response({
                'customer_error': self.customer_does_not_exist_message
            },
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        try:
            Customer.objects.get(user=request.user)
        except Customer.DoesNotExist:
            return super().create(request, *args, **kwargs)
        return Response({
            'customer_error': 'customer already exists'
        })

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        try:
            instance = self.get_queryset().get(user=request.user)
        except Customer.DoesNotExist:
            return Response({
                'customer_error': self.customer_does_not_exist_message
            },
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_queryset().get(user=request.user)
        except Customer.DoesNotExist:
            return Response({
                'customer_error': self.customer_does_not_exist_message
            },
                status=status.HTTP_404_NOT_FOUND
            )
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def create_order(self, request, *args, **kwargs):
        pass
