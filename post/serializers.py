from rest_framework.serializers import ModelSerializer
from .models import Post, Comment, Like
from rest_framework import serializers
from misc.serializers import ImageSerializer 
from user.serializers import LimitedUserSerializer
from user.models import User
from misc.models import Image

class PostSerializer(ModelSerializer):
    likes_count = serializers.SerializerMethodField()
    post_images = ImageSerializer(many=True)
    user_id = LimitedUserSerializer()

    class Meta:
        model = Post
        fields = ('id', 'title', 'description', 'likes_count',  'publish_date', 'user_id', 'category', 'post_images')
        
    def get_likes_count(self, obj):
        return Like.objects.filter(post_id=obj.id).count()

class CreatePostSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(write_only=True)
    post_images = serializers.ListField(
        child=serializers.ImageField(), write_only=True, required=False
    )

    class Meta:
        model = Post
        fields = ('description', 'title', 'user_id', 'category', 'post_images')

    def create(self, validated_data):
        user_id = validated_data.pop('user_id')
        post_images_data = validated_data.pop('post_images', [])
        user = User.objects.get(id=user_id)
        post = Post.objects.create(user_id=user, **validated_data)
        
        for image_data in post_images_data:
            image = Image.objects.create(file=image_data)
            post.post_images.add(image)
        
        return post

class CommentSerializer(ModelSerializer):
    user_id = LimitedUserSerializer()
    class Meta:
        model = Comment
        fields = ('id', 'contents', 'publish_date', 'post_id', 'user_id')
        read_only_fields = ['user_id', 'post_id', 'publish_date']

class CreateCommentSerializer(ModelSerializer):
    user_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = Comment
        fields = ('contents', 'publish_date', 'post_id', 'user_id')

    def create(self, validated_data):
        user_id = validated_data.pop('user_id')
        user = User.objects.get(id=user_id)
        comment = Comment.objects.create(user_id=user, **validated_data)
        return comment

class LikeSerializer(ModelSerializer):
    class Meta:
        model = Like
        fields = ('id', 'like_date', 'post_id', 'user_id')
        # read_only_fields = ('like_date')

class CreateLikeSerializer(ModelSerializer):
    class Meta:
        model = Like
        fields = ('post_id', 'user_id')