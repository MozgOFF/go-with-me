from rest_framework import serializers
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.models import BaseUserManager
from phonenumber_field.serializerfields import PhoneNumberField
from .models import OTP, SMSMessage
from event.models import Category
from files.models import UserImages
from django.utils import timezone

User = get_user_model()


class EmptySerializer(serializers.Serializer):
    pass


class UserCreateSerializer(serializers.ModelSerializer):
    date_joined = serializers.ReadOnlyField()

    class Meta(object):
        model = User
        fields = ('phone', 'email', 'first_name', 'last_name', 'password', 'telegram_username', 'date_joined', 'favorite_category')
        extra_kwargs = {'password': {'write_only': True}}

    @staticmethod
    def validate_email(value):
        # if not value.strip():
        #     raise serializers.ValidationError("email should not be empty")
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("email should be unique")
        return BaseUserManager.normalize_email(value)

    @staticmethod
    def validate_phone(value):
        verifiedPhone = OTP.objects.filter(phone=value)
        if not verifiedPhone.exists() or not verifiedPhone.first().verified:
            raise serializers.ValidationError("Phone is not verified")
        return value

    @staticmethod
    def validate_favorite_category(value):
        print(value)
        if len(value) < 1:
            raise serializers.ValidationError("favorite_category at ")
        return value

    @staticmethod
    def validate_first_name(value):
        if value is None or len(value) == 0:
            raise serializers.ValidationError("validate_first_name")
        return value

    @staticmethod
    def validate_last_name(value):
        if value is None or len(value) == 0:
            raise serializers.ValidationError("validate_first_name")
        return value

    def create(self, validated_data):
        phone = validated_data['phone']
        email = ""
        password = validated_data['password']
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        telegram_username = validated_data.get('telegram_username')
        favorite_category = validated_data.get('favorite_category')

        categories = Category.objects.filter(id__in=[c.id for c in favorite_category])

        user = User(phone=phone,
                    email=email,
                    telegram_username=telegram_username,
                    first_name=first_name,
                    last_name=last_name)
        user.set_password(password)
        user.save()
        for c in categories:
            user.favorite_category.add(c)
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
    is_me_follower = serializers.SerializerMethodField()

    def get_is_me_follower(self, obj):
        request = self.context.get('request')
        if request is None:
            return False
        user = request.user
        if user.id is None:
            return False

        return obj in user.following.get_queryset()

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

