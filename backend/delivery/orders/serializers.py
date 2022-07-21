from rest_framework import serializers
from .models import Order, OrderItem, MenuItem
from authentication.serializers import UserPublicSerializer

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    subtotal = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = OrderItem
        fields = [
            'name',
            'quantity',
            'subtotal'
        ]

    def get_subtotal(self, obj):
        return "%.2f" % (float(obj.item.price) * int(obj.quantity))

    def get_name(self, obj):
        return obj.item.name


class OrderSerializer(serializers.ModelSerializer):
    customer = UserPublicSerializer(read_only=True)
    items = OrderItemSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Order
        fields = [
            'order_status',
            'customer',
            'delivery_at',
            'address',
            'items',
            'total'
        ]

    def get_total(self, obj):
        sum = 0
        order_items = obj.items.all()
        for order_item in order_items:
            sum += float(order_item.item.price) * int(order_item.quantity)
        return "%.2f" % sum
