from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
class Bookmark(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.TextField(blank=True)
    description = models.TextField(blank=True)
    custom_name=models.CharField(max_length=255)
    url=models.URLField(blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    favicon=models.URLField(blank=True)

    def __str__(self):
        return self.title or self.url