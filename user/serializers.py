from rest_framework import serializers
from .models import User, Image

class UserSerializer(serializers.ModelSerializer):
    profile_image = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'name', 'first_name', 'last_name', 'bio', 'email', 'phone', 'profile_image', 'follower_count', 'following_count']
    
    def get_profile_image(self, obj):
        if obj.profile_image:
            return obj.profile_image.file.url
        return None

    def get_follower_count(self, obj):
        return obj.follower_count()

    def get_following_count(self, obj):
        return obj.following_count()
        
class LimitedUserSerializer(serializers.ModelSerializer):
    profile_image = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['name', 'profile_image', 'id']

    def get_profile_image(self, obj):
        if obj.profile_image:
            return obj.profile_image.file.url
        return None