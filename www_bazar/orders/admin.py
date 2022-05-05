from django.contrib import admin
from .models import Order, OrderItem, Kupon


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'fio',  'email', 'delivery', 'bazar',
                    'payment', 'city', 'created', 'updated', 'oplata']
    list_filter = ['oplata', 'created', 'updated']
    inlines = [OrderItemInline]

admin.site.register(Order, OrderAdmin)

class KuponAdmin(admin.ModelAdmin):
    pass
    list_display = ['code', 'valid_from', 'valid_to', 'discount', 'active']
    list_filter = ['active', 'valid_from', 'valid_to']
    search_fields = ['code']
admin.site.register(Kupon, KuponAdmin)

