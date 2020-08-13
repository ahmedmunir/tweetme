from django.urls import path

from tweets.views import (
    home_view,
    tweet_create,
    tweet_list_view,
    tweet_delete, 
    tweet_react,
)

urlpatterns = [
    path('', tweet_list_view, name='tweets'),
    path('create/', tweet_create, name='tweet-create'),
    path('<int:tweet_id>/delete/', tweet_delete, name="tweet-delete"),
    path('<int:tweet_id>/react/', tweet_react, name='tweet-react'),
]