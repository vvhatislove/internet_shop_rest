from django.urls import path

from order.api import OrderViewSet, CustomerViewSet

urlpatterns = [
    path('customer-info/', CustomerViewSet.as_view(
        {
            'get': 'retrieve',
            'post': 'create',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy',
        }
    )),
    path('make-order/', OrderViewSet.as_view({'post': 'create'}))
]
