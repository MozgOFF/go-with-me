from rest_framework import serializers
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.models import BaseUserManager

User = get_user_model()

class UserCreateSerializer(serializers.ModelSerializer):
    
    date_joined = serializers.ReadOnlyField()

    class Meta(object): 
        model = User
        fields = ('phone', 'email', 'password', 'date_joined')
        extra_kwargs = {'password': {'write_only': True}}

    def validate_email(self, value):
        if (not value.strip()):
            raise serializers.ValidationError("email should not be empty")
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("email should be unique")
        return BaseUserManager.normalize_email(value)


    def create(self, validated_data):
        phone = validated_data['phone']
        email = validated_data['email']
        password = validated_data['password']
        
        user = User(phone = phone, email = email)
        user.set_password(password)
        user.save()

        return user

class PasswordChangeSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_current_password(self, value):
        if not self.context['request'].user.check_password(value):
            raise serializers.ValidationError("Current password does not match")
        return value

    def validate_new_password(self, value):
        password_validation.validate_password(value)
        return value

class EmptySerializer(serializers.Serializer):
    pass