from rest_framework import generics, status
from .models import Order

# Create your views here.
class OrderListView(generics.ListCreateAPIView):
    queryset = Order.objects.all().order_by('-delivery_at')
    serializer_class = NoteSerializer