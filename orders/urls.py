from django.urls import path

from . import views


urlpatterns = [
    path('menu/', views.MenuItemPublicListCreateView.as_view(), name='menu'),
    path('menu/<int:pk>/', views.MenuItemDetailUpdateDeleteView.as_view(), name='menu_item'),
    path('orders/', views.OrderListCreateView.as_view(), name='orders'),
    path('orders/<int:pk>/', views.OrderDetailUpdateDeleteView.as_view(), name='order'),
    path('users/<int:user_pk>/orders/', views.UserOrdersListCreateView.as_view(), name='user_orders_list'),
    path('users/<int:user_pk>/orders/<int:order_pk>/',
         views.UserOrderDetailUpdateDeleteView.as_view(), name='user_order_detail'),
]