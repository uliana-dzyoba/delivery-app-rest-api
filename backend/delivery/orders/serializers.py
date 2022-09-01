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
        read_only_fields = ('order',)


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


class OrderItemInlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['name']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemPublicSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Order
        fields = [
            'order_status',
            'delivery_at',
            'address',
            'items',
            'total'
        ]

    def get_total(self, obj):
        total_sum = 0
        order_items = obj.items.all()
        for order_item in order_items:
            total_sum += float(order_item.item.price) * int(order_item.quantity)
        return "%.2f" % total_sum


class OrderCustomerSerializer(OrderSerializer):
    customer = UserPublicSerializer(read_only=True)

    class Meta:
        model = Order
        fields = OrderSerializer.Meta.fields + ['id', 'customer']


class OrderCreateSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            'delivery_at',
            'address',
            'items',
        ]

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            try:
                menu_item = item_data.pop('item')
            except MenuItem.DoesNotExist:
                # We have no object! Do something...
                return None
            OrderItem.objects.create(item=menu_item, order=order, **item_data)
        return order


class OrderAdminCreateSerializer(OrderCreateSerializer):
    class Meta:
        model = Order
        fields = OrderCreateSerializer.Meta.fields + ['customer']
