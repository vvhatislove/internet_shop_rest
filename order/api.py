from rest_framework import permissions
from rest_framework import viewsets, status
from rest_framework.response import Response

from cart.models import Cart
from order.models import Order, Customer
from order.serializers import CustomerSerializer
from order.utils import send_order_email


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


class OrderViewSet(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request):
        # Checking if the cart exists
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            return self._cart_is_empty()
        # Getting items from the cart
        items = cart.cartitem_set.all()
        # Checking that the cart is not empty
        if not len(items):
            return self._cart_is_empty()
        # Check if a customer has been created
        try:
            customer = Customer.objects.get(user=request.user)
        except Customer.DoesNotExist:
            return self._cart_is_empty()
        # Create a list of products that are out of stock
        out_of_stock_products = []
        for item in items:
            # Checking the availability of products in stock
            if item.product.stock - item.quantity < 0:
                out_of_stock_products.append({'id': item.product.pk, 'name': item.product.name})
        # If the list is not empty, we return products that are not available in the required quantity
        if len(out_of_stock_products):
            return Response({
                'Out of stock in the required quantity': out_of_stock_products
            })
        # Create an order
        order = Order.objects.create(customer=customer,
                                     total_cost=sum([item.product.price * item.quantity for item in items]))
        # Add items from the cart to the order
        for item in items:
            order.orderitem_set.create(product=item.product,
                                       price=item.product.price,
                                       quantity=item.quantity)
            # Remove the quantity of products in stock
            item.product.stock -= item.quantity
            item.product.save()
        # Removing items from the cart
        items.delete()
        send_order_email(order)
        return Response({
            'Order number': order.pk
        })

    @staticmethod
    def _cart_is_empty():
        return Response({
            'order_error': 'Cart is empty'
        }, status=status.HTTP_404_NOT_FOUND)

    @staticmethod
    def _no_customer_data():
        return Response({
            'order_error': 'No customer data provided'
        }, status=status.HTTP_404_NOT_FOUND)
