from django.urls import path
from . import views

urlpatterns = [
    path('orders/',views.OrderListCreateView.as_view(),name='orders'),
    path('orders/<int:pk>/', views.OrderDetailStatusView.as_view(), name='order'),
    # path('order/<int:order_id>/update-status/',views.UpdateOrderStatusView.as_view(),name='update_order_status'),
    path('users/<int:user_pk>/orders/',views.UserOrdersListView.as_view(),name='view_user_orders'),
    # path('users/<int:user_pk>/orders/<int:order_pk>/',views.UserOrderDetailView.as_view(),name='user_order_detail'),
]