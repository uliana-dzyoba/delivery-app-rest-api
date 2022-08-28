from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializers import UserSignUpSerializer


# Create your views here.
class UserSignUpView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSignUpSerializer
