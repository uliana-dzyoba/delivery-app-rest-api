from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import generics
from django.db.models import Value

from authentication.mixins import UserQuerySetMixin
from authentication.permissions import IsAdminOrIsOwnerReadOnly, IsAdminOrReadOnly
from .models import Order, MenuItem
from .serializers import OrderSerializer, MenuItemSerializer, OrderCreateSerializer,\
    OrderCustomerSerializer, OrderAdminCreateSerializer
from .mixins import OrderStatusDateFilterMixin

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


# Create your views here.

# for swagger
status_param = openapi.Parameter('status', openapi.IN_QUERY, description="Order status in lowercase", type=openapi.TYPE_STRING)
date_param = openapi.Parameter('date', openapi.IN_QUERY, description="A date in format YYYY-MM-DD", type=openapi.TYPE_STRING)
start_date_param = openapi.Parameter('from', openapi.IN_QUERY, description="Start date in format YYYY-MM-DD", type=openapi.TYPE_STRING)
end_date_param = openapi.Parameter('to', openapi.IN_QUERY, description="End date in format YYYY-MM-DD", type=openapi.TYPE_STRING)


class OrderListCreateView(OrderStatusDateFilterMixin, UserQuerySetMixin, generics.ListCreateAPIView):
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

    # for swagger
    @method_decorator(decorator=swagger_auto_schema(
        manual_parameters=[status_param, date_param, start_date_param, end_date_param]
    ))
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class OrderDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsAdminOrIsOwnerReadOnly]
    queryset = Order.objects.all()
    serializer_class = OrderCustomerSerializer


# view specifically for staff only
class UserOrdersListCreateView(OrderStatusDateFilterMixin, generics.ListCreateAPIView):
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
        if self.request.method == 'POST':
            kwargs["context"] = self.get_serializer_context()
            draft_request_data = self.request.data.copy()
            draft_request_data["customer"] = self.kwargs.get('user_pk')
            kwargs["data"] = draft_request_data
        return serializer_class(*args, **kwargs)

    def get_queryset(self):
        if self.kwargs.get('user_pk'):
            return self.queryset.filter(customer=self.kwargs.get('user_pk'))
        return self.queryset.all()

    # for swagger
    @method_decorator(decorator=swagger_auto_schema(
        manual_parameters=[status_param, date_param, start_date_param, end_date_param]
    ))
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


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


class MenuItemPublicListCreateView(generics.ListCreateAPIView):
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


class MenuItemDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminOrReadOnly]
    queryset = Order.objects.all()
    serializer_class = MenuItemSerializer
