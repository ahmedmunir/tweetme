from django.db import models
from django.utils import timezone

# Create your models here.
class Tweet(models.Model):
    content     = models.TextField(max_length=250, blank=True, null=True)
    image       = models.ImageField(upload_to="tweets/images/", blank=True, null=True)
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Tweet: {self.content}"

    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "date_posted": self.date_posted
        }