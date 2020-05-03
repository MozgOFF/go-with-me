from rest_framework import serializers
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.models import BaseUserManager
from phonenumber_field.serializerfields import PhoneNumberField
from .models import OTP, SMSMessage
from files.models import UserImages
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

    @staticmethod
    def validate_email(value):
        if not value.strip():
            raise serializers.ValidationError("email should not be empty")
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("email should be unique")
        return BaseUserManager.normalize_email(value)

    @staticmethod
    def validate_phone(value):
        verifiedPhone = OTP.objects.filter(phone=value)
        if not verifiedPhone.exists() or not verifiedPhone.first().verified:
            raise serializers.ValidationError("Phone is not verified")
        return value

    def create(self, validated_data):
        phone = validated_data['phone']
        email = validated_data['email']
        password = validated_data['password']

        user = User(phone=phone, email=email)
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

    @staticmethod
    def validate_new_password(value):
        password_validation.validate_password(value)
        return value


class CheckPhoneSerializer(serializers.Serializer):
    phone = PhoneNumberField(required=True)

    @staticmethod
    def validate_phone(value):
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

    @staticmethod
    def validate_phone(value):
        if not OTP.objects.filter(phone=value).exists():
            raise serializers.ValidationError("There is not such phone number")
        return value

    @staticmethod
    def validate_code(value):
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
        if timezone.now() - otp.updated > timezone.timedelta(minutes=1):
            raise serializers.ValidationError("Time is up")

        otp.verified = True
        otp.save()
        return otp


class SMSMessageSerializer(serializers.ModelSerializer):
    content = serializers.CharField(required=True)

    class Meta(object):
        model = SMSMessage
        fields = ('content',)


class ProfileImageSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = UserImages
        fields = ['image', 'description']


class ShortProfileInfoSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    @staticmethod
    def get_image(obj):
        query_set = UserImages.objects.filter(user=obj).first()
        serializer = ProfileImageSerializer(query_set)
        return serializer.data

    class Meta:
        model = User
        fields = ['id',
                  'first_name',
                  'last_name',
                  'image',
                  ]


class ProfileInfoSerializer(serializers.ModelSerializer):
    events_created_count = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    saved_events_count = serializers.SerializerMethodField()

    @staticmethod
    def get_events_created_count(obj):
        return obj.event_set.all().count()

    @staticmethod
    def get_followers_count(obj):
        return User.objects.filter(following=obj).count()

    @staticmethod
    def get_following_count(obj):
        return obj.following.all().count()

    @staticmethod
    def get_images(obj):
        query_set = UserImages.objects.filter(user=obj)
        serializer = ProfileImageSerializer(query_set, many=True)
        return serializer.data

    @staticmethod
    def get_saved_events_count(obj):
        return obj.saved_events.count()

    class Meta:
        model = User
        # fields = '__all__'
        exclude = ['password',
                   'groups',
                   'user_permissions',
                   'following',
                   'date_joined',
                   'is_active',
                   'is_staff',
                   'is_superuser',
                   ]

