from django.contrib import admin
from .models import Category, Tag, Post, Comment, Like

# Register your models here.

admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)