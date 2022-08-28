from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import generics
from django.db.models import Value
from .models import Order, MenuItem
from .serializers import OrderSerializer, MenuItemSerializer, OrderCreateSerializer,\
    OrderCustomerSerializer, OrderAdminCreateSerializer
from authentication.mixins import UserQuerySetMixin
from authentication.permissions import IsOwnerPermission, IsAdminOrReadOnly


# Create your views here.

class OrderListCreateView(UserQuerySetMixin, generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all().order_by('-delivery_at')
    serializer_class = OrderSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            if self.request.user.is_staff:
                return OrderAdminCreateSerializer
            return OrderCreateSerializer
        # for the staff the customer of the order is shown
        elif self.request.user.is_staff:
            return OrderCustomerSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        # if order is created by admin they need to specify the user
        if not self.request.user.is_staff:
            serializer.save(customer=self.request.user)
        serializer.save()


class OrderDetailStatusDeleteView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsOwnerPermission]
    queryset = Order.objects.all()
    serializer_class = OrderCustomerSerializer

    # for updating the order status PATCH method is used
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


# view specifically for staff only
class UserOrdersListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = Order.objects.all().order_by('-delivery_at')
    serializer_class = OrderCustomerSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OrderAdminCreateSerializer
        return self.serializer_class

    # set customer from user_pk
    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs["context"] = self.get_serializer_context()
        draft_request_data = self.request.data.copy()
        draft_request_data["customer"] = self.kwargs.get('user_pk')
        kwargs["data"] = draft_request_data
        return serializer_class(*args, **kwargs)

    def get_queryset(self):
        if self.kwargs.get('user_pk'):
            return self.queryset.filter(customer=self.kwargs.get('user_pk'))
        return self.queryset.all()


# view specifically for staff only
class UserOrderDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = Order.objects.all()
    serializer_class = OrderCustomerSerializer

    def get_object(self):
        if self.kwargs.get('user_pk'):
            return get_object_or_404(self.get_queryset(), customer=self.kwargs.get('user_pk'),
                                     pk=self.kwargs.get('order_pk'))
        return get_object_or_404(self.get_queryset(), pk=self.kwargs.get('order_pk'))


class MenuItemPublicListView(generics.ListCreateAPIView):
    permission_classes = [IsAdminOrReadOnly]
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    def get_queryset(self):
        qs1 = MenuItem.objects.filter(category='AP').annotate(custom_order=Value(1))
        qs2 = [MenuItem.objects.filter(category='SP').annotate(custom_order=Value(2)),
               MenuItem.objects.filter(category='SL').annotate(custom_order=Value(3)),
               MenuItem.objects.filter(category='DS').annotate(custom_order=Value(4)),
               MenuItem.objects.filter(category='DR').annotate(custom_order=Value(5)),
               MenuItem.objects.filter(category='OT').annotate(custom_order=Value(6))]

        qs = qs1.union(*qs2).order_by('custom_order')
        return qs


class MenuItemUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminOrReadOnly]
    queryset = Order.objects.all()
    serializer_class = MenuItemSerializer
