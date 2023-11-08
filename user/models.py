from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=30, blank=True, null=True)
    confirm_password = models.CharField(max_length=30, default='', blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    phone_number = PhoneNumberField(unique=True, blank=True, null=True)
    profile_picture = models.ImageField(blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    status = models.BooleanField(default=False)
    birth_date = models.DateField(blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()
    USERNAME_FIELD = 'username'


class UserFriend(models.Model):
    source_id = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='user_friends')
    target_id = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    status = models.SmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    notes = models.CharField(max_length=500)


class UserMessage(models.Model):
    source_id = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='sent_messages')
    target_id = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class UserFollower(models.Model):
    source_id = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='followers')
    target_id = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='following')
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
