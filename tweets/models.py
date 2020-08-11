from django.db import models
from django.utils import timezone

from users.models import NewUser

# Create your models here.
class Tweet(models.Model):
    content     = models.TextField(max_length=250, blank=True, null=True)
    image       = models.ImageField(upload_to="tweets/images/", blank=True, null=True)
    date_posted = models.DateTimeField(default=timezone.now)
    author      = models.ForeignKey(NewUser, on_delete=models.CASCADE, related_name='tweets')

    def __str__(self):
        return f"Tweet: {self.content}"
