from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserCreateSerializer(serializers.ModelSerializer):
    
    date_joined = serializers.ReadOnlyField()

    class Meta(object): 
        model = User
        fields = ('phone', 'email', 'password', 'date_joined')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        phone = validated_data['phone']
        email = validated_data['email']
        password = validated_data['password']
        
        if (not email.strip()):
            raise serializers.ValidationError("email should not be empty")
        
        if (email and User.objects.filter(email = email).exclude(phone = phone).exists()):
            raise serializers.ValidationError("email should be unique")

        user = User(phone = phone, email = email)
        user.set_password(password)
        user.save()

        return user

class UserSerializer(serializers.ModelSerializer):

    