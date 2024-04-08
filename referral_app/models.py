from django.db import models
from django.utils import timezone
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
import secrets
import string


class UserManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email required')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be a staff'
            )
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be a superuser'
            )

        return self._create_user(email, password, **extra_fields)


class UserModel(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, max_length=255, blank=False)
    name = models.CharField(max_length=255)
    refer_code = models.CharField(
        max_length=50, blank=True, null=True, unique=True)
    referral_code = models.CharField(max_length=50, blank=True, null=True)
    referral_point = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField('staff status', default=False)
    is_active = models.BooleanField('active', default=True)
    is_superuser = models.BooleanField('superuser', default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    alphanumeric = string.ascii_letters + string.digits
    # It will genrate unique refer code

    def save(self, *args, **kwargs):
        if not self.refer_code:
            self.refer_code = ''.join(secrets.choice(
                self.alphanumeric) for _ in range(6))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email


class Referral(models.Model):
    user = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, related_name='referrals')
    referred_by = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, related_name='referred_by')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'referred_by')

    def save(self, *args, **kwargs):
        self.referred_by.referral_point += 1
        self.referred_by.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'User: {self.user.id} is referred by {self.referred_by.id}'
