from rest_framework import generics, filters
from rest_framework.permissions import AllowAny, IsAdminUser
from django.contrib.auth import get_user_model
from .serializers import UserSignUpSerializer, UserPublicSerializer, UserSerializer


# Create your views here.
class UserSignUpView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSignUpSerializer


class UserListView(generics.ListAPIView):
    permission_classes = [IsAdminUser]
    queryset = get_user_model().objects.all()
    serializer_class = UserPublicSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'email']


class UserDetailDeleteView(generics.RetrieveDestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

