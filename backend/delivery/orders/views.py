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

class OrderDetailStatusView(UserQuerySetMixin, generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsOwnerPermission]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    # def patch(self, request, pk):
    #     testmodel_object = self.get_object(pk)
    #     serializer = TestModelSerializer(testmodel_object, data=request.data, partial=True)  # set partial=True to update a data partially
    #     if serializer.is_valid():
    #         serializer.save()
    #         return JsonResponse(code=201, data=serializer.data)
    #     return JsonResponse(code=400, data="wrong parameters")


class MenuItemListView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all().order_by('name')
    serializer_class = MenuItemSerializer