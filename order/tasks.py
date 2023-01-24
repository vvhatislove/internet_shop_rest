from django.core.mail import send_mail

from internet_shop_rest import settings
from internet_shop_rest.celery import app
from order.models import Order
from order.utils import send_order_report


@app.task
def send_order_report_by_email(order_pk: int, title: str = 'Django Shop'):
    send_order_report(order_pk=order_pk, title=title)
