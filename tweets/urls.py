from django.urls import path

from tweets.views import (
    home_view,
    tweet_create,
    tweet_list_view,
    tweet_delete, 
    tweet_react,
    tweet_retweet,
    tweet_edit,
    search_template,
    search_list_tweets
)

urlpatterns = [
    path('', tweet_list_view, name='tweets'),
    path('create/', tweet_create, name='tweet-create'),
    path('search/', search_template, name="search_template"),
    path('list_search_tweets/', search_list_tweets, name='tweets_search_list'),
    path('<int:tweet_id>/delete/', tweet_delete, name="tweet-delete"),
    path('<int:tweet_id>/react/', tweet_react, name='tweet-react'),
    path('<int:tweet_id>/retweet/', tweet_retweet, name='tweet-retweet'),
    path('<int:tweet_id>/edit/', tweet_edit, name='tweet-edit')
]