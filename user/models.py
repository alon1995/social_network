from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, User
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    user_name = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=30)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    phone_number = PhoneNumberField(unique=True)
    profile_picture = models.ImageField()
    about = models.TextField()
    status = models.BooleanField(default=False)
    birth_date = models.DateField()
    is_staff = models.BooleanField(default=False)
    last_login = User.last_login

    USERNAME_FIELD = 'user_name'


class UserFriend(models.Model):
    source_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    target_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    status = models.SmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    notes = models.CharField(max_length=500)


class UserMessage(models.Model):
    source_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    target_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class UserFollower(models.Model):
    source_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    target_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
