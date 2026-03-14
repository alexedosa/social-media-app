from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import make_password

class CreateAccountSerializer(serializers.ModelSerializer): # Use ModelSerializer
    password = serializers.CharField(write_only=True) # Changed to singular

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def validate_email(self, value):
        if User.objects.filter(email=value).exists(): # Added 's' to objects
            raise serializers.ValidationError("Email already exists")
        return value
    
    def create(self, validated_data):
        # Hash the password before saving
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            password=make_password(validated_data['password']) 
        )
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data): # DRF uses 'validate', not 'CheckAuthentication'
        try:
            user = User.objects.get(email=data['email'])
        except User.DoesNotExist:
            raise serializers.ValidationError('Invalid Credentials.')
        
        # Verify the hashed password
        if not user.check_password(data['password']):
            raise serializers.ValidationError('Invalid Credentials.')
            
        data['user'] = user
        return data
