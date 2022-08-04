from django.urls import path
from . import views

urlpatterns = [
    path('orders/',views.OrderListCreateView.as_view(),name='orders'),
    path('orders/<int:pk>/', views.OrderDetailStatusDeleteView.as_view(), name='order'),
    # path('order/<int:order_id>/update-status/',views.UpdateOrderStatusView.as_view(),name='update_order_status'),
    path('users/<int:user_pk>/orders/', views.UserOrdersListView.as_view(), name='user_orders_list'),
    path('users/<int:user_pk>/orders/<int:order_pk>/', views.UserOrderDetailUpdateDeleteView.as_view(), name='user_order_detail'),
]