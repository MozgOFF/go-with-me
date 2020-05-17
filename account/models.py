from django.db import models, transaction
from django.contrib.auth.models import AbstractUser, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField
import random


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, phone, password, **extra_fields):
        if not phone:
            raise ValueError("The given phone must be set")
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(phone, password, **extra_fields)

    def create_superuser(self, phone, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(phone, password, **extra_fields)


class User(AbstractUser):
    username = None

    phone = PhoneNumberField(unique=True, help_text='Phone number')
    following = models.ManyToManyField('self',
                                       through='Friendships',
                                       related_name='followers',
                                       related_query_name='followers',
                                       through_fields=('from_user', 'to_user'))

    # remove blank=True
    latitude = models.DecimalField(verbose_name="Latitude", max_digits=17, decimal_places=14, null=True)
    longitude = models.DecimalField(verbose_name="Longitude", max_digits=17, decimal_places=14, null=True)

    telegram_username = models.CharField(verbose_name="telegram_username", max_length=100, blank=True, null=True)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    objects = UserManager()

    def __str__(self):
        return self.phone.__str__()


class Friendships(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_user')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_user')
    isAccepted = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return "{} -> {}".format(self.from_user.phone, self.to_user.phone)


class SMSMessage(models.Model):
    content = models.CharField(verbose_name="Content", max_length=255, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content.__str__()


class OTP(models.Model):
    phone = PhoneNumberField(unique=True, help_text='Phone number')
    code = models.CharField(verbose_name='Verification code', max_length=4)
    verified = models.BooleanField(verbose_name="Verified", default=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    @classmethod
    def generate(cls, phone: PhoneNumberField):
        code = random.randint(1000, 9999)
        if cls.objects.filter(phone=phone).exists():
            obj = cls.objects.get(phone=phone)
            obj.code = code
            obj.save()
        else:
            instance = cls(phone=phone, code=code)
            instance.save()
        return code

    def __str__(self):
        return "{} - verified: {}".format(self.phone, self.verified)
