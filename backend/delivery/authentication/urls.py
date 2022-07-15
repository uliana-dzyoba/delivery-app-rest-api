from django.urls import path
from . import views

urlpatterns = [
    path('signup/',views.AuthView.as_view(),name='sign_up'),
]