from django.urls import path
from . import views

urlpatterns = [
    path('', views.UserSignUpView.as_view(), name='sign_up'),
]