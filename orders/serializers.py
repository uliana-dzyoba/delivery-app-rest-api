from rest_framework import serializers

from authentication.serializers import UserPublicSerializer
from .models import Order, OrderItem, MenuItem


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = '__all__'


# serializer used in order creation
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'
        read_only_fields = ('order',)


# serializer used to view orderitem in order
class OrderItemPublicSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='item.name', read_only=True)
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = [
            'name',
            'quantity',
            'subtotal'
        ]

    def get_subtotal(self, obj):
        return f'{(obj.item.price * obj.quantity):.2f}'


# basic view order serializer
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemPublicSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()

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
        total_sum = sum([order_item.item.price * order_item.quantity for order_item in obj.items.all()])
        return f'{total_sum:.2f}'


class OrderCustomerSerializer(OrderSerializer):
    customer = UserPublicSerializer(read_only=True)

    class Meta:
        model = Order
        fields = OrderSerializer.Meta.fields + ['id', 'customer']


class OrderCreateSerializer(serializers.ModelSerializer):
    # example:
    # {
    #     "items": [{"item": 1, "quantity": 2}],
    #     "address": "Adr.Str."
    # }
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
                raise serializers.ValidationError("The menu item does not exist")
            OrderItem.objects.create(item=menu_item, order=order, **item_data)
        return order


class OrderAdminCreateSerializer(OrderCreateSerializer):
    class Meta:
        model = Order
        fields = OrderCreateSerializer.Meta.fields + ['customer']
