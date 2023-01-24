from django.core.mail import send_mail

from internet_shop_rest import settings
from order.models import Order


def create_message(order: Order):
    message = f'''Order №{order.pk}
Date added: {order.date}

Delivery data:
    Name: {order.customer.name}
    Email: {order.customer.email}
    Phone: {order.customer.phone}
    Address: {order.customer.address}
    Postal code: {order.customer.postal_code}
    City: {order.customer.city}

Products:
'''
    for item in order.orderitem_set.all():
        message += f'Name: {item.product.name}\n' \
                   f'Vendor code: {item.product.vendor_code}\n' \
                   f'Quantity: {item.quantity}\n' \
                   f'Price: {item.product.price}\n' \
                   f'Total: {item.product.price * item.quantity}\n\n\n'
    message += f'\nTOTAL: {order.total_cost}'
    return message


def send_order_report(order_pk: int, title: str):
    order = Order.objects.get(pk=order_pk)
    title = title + f' Order №{order.pk}'
    message = create_message(order)
    send_mail(title, message, settings.EMAIL_HOST_USER, [order.customer.email], fail_silently=False)
