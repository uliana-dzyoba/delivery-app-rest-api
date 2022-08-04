from django.shortcuts import render,get_object_or_404
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework import generics, status
from .models import Order, MenuItem
from .serializers import OrderSerializer, MenuItemSerializer, OrderCreateSerializer
from authentication.mixins import UserQuerySetMixin
from authentication.permissions import IsOwnerPermission

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
        serializer.save(customer=self.request.user)

class OrderDetailStatusDeleteView(UserQuerySetMixin, generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsOwnerPermission]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


class UserOrdersListView(generics.ListAPIView):
    permission_classes = [IsAdminUser]
    queryset = Order.objects.all().order_by('-delivery_at')
    serializer_class = OrderSerializer

    def get_queryset(self):
        if self.kwargs.get('user_pk'):
            return self.queryset.filter(customer=self.kwargs.get('user_pk'))
        return self.queryset.all()


class UserOrderDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_object(self):
        if self.kwargs.get('user_pk'):
            return get_object_or_404(self.get_queryset(), customer=self.kwargs.get('user_pk'), pk=self.kwargs.get('order_pk'))
        return get_object_or_404(self.get_queryset(), pk=self.kwargs.get('order_pk'))


class MenuItemListView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all().order_by('name')
    serializer_class = MenuItemSerializer