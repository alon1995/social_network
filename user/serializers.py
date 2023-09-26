from rest_framework import serializers
from user.models import *


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
    
class UserFriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFriend
        fields = '__all__'

class UserMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMessage
        fields = '__all__'

class UserFollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFollower
        fields = '__all__'

