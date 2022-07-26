from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework import generics, status
from .models import Order, MenuItem
from .serializers import OrderSerializer, MenuItemSerializer, OrderCreateSerializer
from authentication.mixins import UserQuerySetMixin

# Create your views here.
class OrderListCreateView(UserQuerySetMixin, generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all().order_by('-delivery_at')
    serializer_class = OrderSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OrderCreateSerializer
        else:
            return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# class OrderCreateView(UserQuerySetMixin, generics.CreateAPIView):
#     permission_classes = [IsAuthenticated]
#     queryset = Order.objects.all()
#     serializer_class = OrderCreateSerializer

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)

class MenuItemListView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all().order_by('name')
    serializer_class = MenuItemSerializer