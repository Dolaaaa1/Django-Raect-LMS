from django.shortcuts import render
from api import serializer as api_serializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from userauths.models import User
from rest_framework.permissions import AllowAny
import random
from rest_framework_simplejwt.tokens import RefreshToken
# Create your views here.

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = api_serializer.MyTokenObtainPairSerializer



class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = api_serializer.RegisterSerializer

def generate_random_otp(length=7):
    otp = ''.join([str(random.randint(0 , 9 )) for _ in range(length)]) 
    return otp
    
class PasswordResetEmailVerifyAPIView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = api_serializer.UserSerializer
    
    def get_object(self):
        email = self.kwargs['email']
        
        user = User.objects.filter(email=email).first()
        
        if user:
            uuidb64 = user.pk
            refresh = RefreshToken.for_user(user)
            refresh_token = str(refresh.access_token)
            
            user.refresh_token = refresh_token
            user.otp = generate_random_otp()
            user.save()
            
            link = f"http://localhost:5173/create-new-password/?otp={user.otp}&uuidb64={uuidb64}&refresh_token={refresh_token} " 
            print("link ======" , link)           
        
        return user
            