from django.urls import path

from order.api import OrderViewSet, CustomerViewSet

urlpatterns = [
    path('customer-info/', CustomerViewSet.as_view(
        {'get': 'get_customer_info',
         'post': 'create'
         }
    ))
]
