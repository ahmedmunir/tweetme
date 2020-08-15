from django.db import models
from django.utils import timezone

from users.models import NewUser

# Create your models here.
class Tweet(models.Model):
    content             = models.TextField(max_length=250, blank=True, null=True)
    image               = models.ImageField(upload_to="tweets/images/", blank=True, null=True)
    date_posted         = models.DateTimeField(default=timezone.now)
    author              = models.ForeignKey(NewUser, on_delete=models.CASCADE, related_name='tweets')
    likes               = models.ManyToManyField(NewUser, related_name='likes')
    dislikes            = models.ManyToManyField(NewUser, related_name='dislikes')
    retweeted_tweet     = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL)
    retweet             = models.BooleanField(default=False)

    def __str__(self):
        return f"Tweet: {self.content}"

    def serializer(self, user):
        return {
            "id": self.id,
            "content": self.content,
            "date_posted": self.date_posted,
            "user_username": self.author.username,
            "user_first_name": self.author.first_name,
            "user_last_name": self.author.last_name,
            "user_image": self.author.image.url,
            "tweet-owner": self.author == user,
            "likes": self.likes.count(),
            "dislikes": self.dislikes.count(),
            "liked": "add" if user in self.likes.all() else "remove",
            "disliked": "add" if user in self.dislikes.all() else "remove",
            "retweeted_tweet": self.retweeted_tweet.serializer(user) if self.retweeted_tweet else self.retweeted_tweet,
            "retweet": self.retweet
        }