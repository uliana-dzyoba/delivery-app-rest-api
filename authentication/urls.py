from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.UserListView.as_view(), name='users'),
    path('users/<int:pk>/', views.UserDetailDeleteView.as_view(), name='user'),
    path('auth/signup/', views.UserSignUpView.as_view(), name='sign_up'),
]
