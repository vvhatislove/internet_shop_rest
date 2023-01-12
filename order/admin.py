from django.contrib import admin

from order.models import Customer, Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'date', 'paid', 'total_cost']
    list_filter = ['date', 'id']
    inlines = [OrderItemInline]


admin.site.register(Order, OrderAdmin)
admin.site.register(Customer)
