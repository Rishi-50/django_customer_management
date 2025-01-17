from rest_framework import serializers
from django.contrib import auth
from customer_management.exceptions import CustomApiException
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken



class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    re_enter_password = serializers.CharField(style={'input_type': 'password'}, write_only=True, required=True)
    tokens = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['full_name', 'email', 'password', 're_enter_password', 'tokens']
        
    def validate(self, data):
        if data.get('password') != data.get('re_enter_password'):
            raise CustomApiException(403,{"sucess":False,"data":{"message":"Passwords must match."}})
        if len(data.get('password')) < 8:
            raise CustomApiException(403,{"sucess":False,"data":{"message":"Password must be at least 8 characters long."}})
        return data
    
    def create(self, validated_data):
        validated_data.pop('re_enter_password', None)
        user = User.objects.create(
        email=validated_data['email'],
        full_name=validated_data['full_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        refresh = RefreshToken.for_user(user)
        user.tokens = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        return user
    
    def get_tokens(self, obj):
        user = User.objects.get(email=obj.email)
        return {
            'refresh': user.tokens()['refresh'],
            'access': user.tokens()['access']
        }

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=68, write_only=True)
    is_valid = serializers.BooleanField(read_only=True)
    tokens = serializers.SerializerMethodField()
    def get_tokens(self, obj):
        user = User.objects.get(email=obj.get('email'))
        return {
            'refresh': user.tokens()['refresh'],
            'access': user.tokens()['access']
        }
    class Meta:
        model = User
        fields = ['email','password','is_valid','tokens']
        
    def validate(self, attrs):
        email = attrs.get('email','')
        password = attrs.get('password','')
        user = auth.authenticate(email=email, password=password)
        if not user:
            raise CustomApiException(403,{"sucess":False,"data":{"message":"Invalid credentials, try again"}})
        return {
        'full_name': user.full_name,
        'email': user.email,
        'tokens': user.tokens,
        'is_active' : user.is_active,
        }

