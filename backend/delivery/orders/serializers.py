from rest_framework import serializers
from .models import Order, OrderItem, MenuItem
from authentication.serializers import UserPublicSerializer

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'

class OrderItemPublicSerializer(serializers.ModelSerializer):
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
    # customer = UserPublicSerializer(source='user', read_only=True)
    customer = UserPublicSerializer(read_only=True)
    items = OrderItemPublicSerializer(many=True, read_only=True)
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


class OrderCreateSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            'customer',
            'delivery_at',
            'address',
            'items',
        ]

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            try:
                mi_id =
                menu_item = MenuItem.objects.get(id=)
            except MenuItem.DoesNotExist:
                # We have no object! Do something...
                pass
            OrderItem.objects.create(order=order, **item_data)
        return order