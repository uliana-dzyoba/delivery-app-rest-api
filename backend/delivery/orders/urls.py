from django.urls import path
from . import views

urlpatterns = [
    path('orders/',views.OrderListCreateView.as_view(),name='orders'),
]