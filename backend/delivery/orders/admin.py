from django.contrib import admin
from .models import Order, MenuItem

# Register your models here.

admin.site.register(MenuItem)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display=['id', 'customer', 'order_status', 'delivery_at', 'address']
    list_filter=['delivery_at', 'order_status', 'created_at', 'updated_at']

