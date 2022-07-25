from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework import generics, status
from .models import Order, MenuItem
from .serializers import OrderSerializer, MenuItemSerializer
from authentication.mixins import UserQuerySetMixin

# Create your views here.
class OrderListView(UserQuerySetMixin, generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all().order_by('-delivery_at')
    serializer_class = OrderSerializer

class OrderCreateView(UserQuerySetMixin, generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all().order_by('-delivery_at')
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class MenuItemListView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all().order_by('name')
    serializer_class = MenuItemSerializer