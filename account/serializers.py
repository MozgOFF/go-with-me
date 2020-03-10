from rest_framework import serializers
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.models import BaseUserManager
from phonenumber_field.serializerfields import PhoneNumberField
from .models import OTP, SMSMessage
from django.utils import timezone

User = get_user_model()

class EmptySerializer(serializers.Serializer):
    pass

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

    def validate_phone(self, value):
        verifiedPhone = OTP.objects.filter(phone=value)
        if not verifiedPhone.exists() or not verifiedPhone.first().verified:
            raise serializers.ValidationError("Phone is not verified")
        return value

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

class CheckPhoneSerializer(serializers.Serializer):
    phone = PhoneNumberField(required=True)

    def validate_phone(self, value):
        print("&&&validate_phone", value)
        
        if User.objects.filter(phone=value).exists():
            raise serializers.ValidationError("Phone already exists")
        return value

    def create(self, validated_data):
        phone = validated_data['phone']
        code = OTP.generate(phone=phone)
        return code

class ConfirmPhoneSerializer(serializers.Serializer):
    phone = PhoneNumberField(required=True)
    code = serializers.CharField(required=True)

    def validate_phone(self, value):
        if not OTP.objects.filter(phone=value).exists():
            raise serializers.ValidationError("There is not such phone number")
        return value
    
    def validate_code(self, value):
        if len(value) != 4:
            raise serializers.ValidationError("Invalied code")
        return value

    def create(self, validated_data):
        phone = validated_data['phone']
        code = validated_data['code']

        if not OTP.objects.filter(phone=phone, code=code).exists():
            raise serializers.ValidationError("Error")
        

        otp = OTP.objects.get(phone=phone, code=code)
        # Вынести время жизни otp
        # продумать ответы ошибок
        if (timezone.now() - otp.updated > timezone.timedelta(minutes=1)):
            raise serializers.ValidationError("Time is up")

        otp.verified = True
        otp.save()
        return otp

class SMSMessageSerializer(serializers.ModelSerializer):
    content = serializers.CharField(required=True)

    class Meta(object):
        model = SMSMessage
        fields = ('content', )
