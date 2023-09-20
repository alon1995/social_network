from django.db import models
from user.models import CustomUser
# Create your models here.


class Post(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    is_liked = models.BooleanField(default=False)
    like_count = models.IntegerField(default=0)


class Comment(models.Model):
    user_id = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    comment_replied_to = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True)
    is_liked = models.BooleanField(default=False)
    like_count = models.IntegerField(default=0)
