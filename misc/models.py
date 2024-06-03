from django.db import models

# Create your models here.

class Category(models.Model):
    #Primary key implicit
    category_name = models.CharField(max_length=64)

    def __str__(self):
        return self.category_name

class Tag(models.Model):
    #Primary key implicit
    tag_name = models.CharField(max_length=64)

    def __str__(self):
        return self.tag_name
    
class Image(models.Model):
    file = models.ImageField(upload_to='images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image {self.id}, {self.file}"
