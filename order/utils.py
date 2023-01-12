from django.core.mail import send_mail

from internet_shop_rest import settings
from order.models import Order


def send_order_email(order: Order, title: str = 'Django Shop'):
    title = title + f' Order №{order.pk}'
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
    send_mail(title, message, settings.EMAIL_HOST_USER, [order.customer.email], fail_silently=False)
