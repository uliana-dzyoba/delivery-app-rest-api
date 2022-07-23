from rest_framework import generics
from .models import User
from .serializers import UserSerializer

# Create your views here.
class UserCreateView(generics.CreateAPIView):
    serializer_class = UserSerializer
