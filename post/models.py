from django.db import models
from user.models import CustomUser
from django.utils import timezone

# Create your models here.

class Category(models.Model):
    #Primary key implicit
    category_name = models.CharField(max_length=50)

    def __str__(self):
        return self.category_name


class Tag(models.Model):
    #Primary key implicit
    tag_name = models.CharField(max_length=50)

    def __str__(self):
        return self.tag_name


class Post(models.Model):
    #Primary key implicit
    title = models.CharField(max_length=50)
    publish_date = models.DateTimeField(default=timezone.now)
    description = models.TextField(null=True)
    #Foreign Keys:
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    category_id = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
    #Many-to-many relations
    post_tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title


class Comment(models.Model):
    #Primary key implicit
    contents = models.TextField()
    publish_date = models.DateTimeField(default=timezone.now)
    #Foreign Keys:
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)


class Like(models.Model):
    like_date = models.DateTimeField(default=timezone.now)
    #Foreign Keys:
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    #Composite Primary Key
    class Meta:
        unique_together = ('post_id', 'user_id')
