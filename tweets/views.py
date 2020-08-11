from django.shortcuts import render
from django.http import  JsonResponse
from django.contrib.auth.decorators import login_required

from tweets.forms import TweetForm
from tweets.models import Tweet
# Create your views here.

# Home Function
def home_view(request, *args, **kwargs):
    form = TweetForm()
    return render(request, "pages/home.html", context={"form": form}, status=200)

# Create Tweet
@login_required
def tweet_create(request, *args, **kwargs):
    form = TweetForm(request.POST)
    if form.is_valid():
        form.instance.author = request.user
        new_tweet = form.save()
        new_tweet_serializer = {
            "id": new_tweet.id,
            "content": new_tweet.content,
            "date_posted": new_tweet.date_posted,
            "user_username": new_tweet.author.username,
            "user_first_name": new_tweet.author.first_name,
            "user_last_name": new_tweet.author.last_name,
            "user_image": new_tweet.author.image.url,
            "tweet-owner": new_tweet.author == request.user,
            "likes": new_tweet.likes.count(),
            "dislikes": new_tweet.dislikes.count(),
            "liked": "add" if request.user in new_tweet.likes.all() else "remove",
            "disliked": "remove" if request.user in new_tweet.dislikes.all() else "remove"
        }
        return JsonResponse({"process": "success", "tweet": new_tweet_serializer})
    return JsonResponse({"process": "failed", "errors": form.errors})
    

# List all Tweets
def tweet_list_view(request, *args, **kwargs):
    """
        REST API View for all Tweets
    """
    
    # Calculate the range of queryset according to user request 
    start = int(request.GET.get('start'))
    end = int(request.GET.get('end'))
    quantity = 10
    count = Tweet.objects.count()
    first_index_at_DB = Tweet.objects.first().pk
    last_index = Tweet.objects.last().pk    
    """
        Query data according to start & end request coming from User
        first_index_at_DB was added to solve the problem if there were data deleted
        last_index was added to solve problem if one of tweets in middle was deleted
    """

    start_range = count - start + first_index_at_DB  if count - start > 0 else 0
    end_range = count - end + first_index_at_DB  if last_index - end  > 0 else 0
    query_set = Tweet.objects.filter(id__range=(end_range, start_range)).order_by("-date_posted")

    # Convert tweets queryset into list to be able to send it through JSON
    tweets = [{
        "id": tweet.id,
        "content": tweet.content,
        "date_posted": tweet.date_posted,
        "user_username": tweet.author.username,
        "user_first_name": tweet.author.first_name,
        "user_last_name": tweet.author.last_name,
        "user_image": tweet.author.image.url,
        "tweet-owner": tweet.author == request.user,
        "likes": tweet.likes.count(),
        "dislikes": tweet.dislikes.count(),
        "liked": "add" if request.user in tweet.likes.all() else "remove",
        "disliked": "add" if request.user in tweet.dislikes.all() else "remove"
    } for tweet in query_set]
    data = {
        "tweets": tweets,
    }
    return JsonResponse(data)

# Delete Tweet 
@login_required
def tweet_delete(request, tweet_id, *args, **kwargs):
    try:
        tweet = Tweet.objects.get(id=tweet_id)
    except:
        return JsonResponse({'message': "Tweet wasn't found"})
    
    # Ensure that the owner of tweet who wants to delete it
    if tweet.author == request.user:
        tweet.delete()
        return JsonResponse({'message': 'TweeT deleted successfully!'})
    else:
        return JsonResponse({'message': "You can't delete tweet because you are not the owner!"})


# Like & Dislike 
@login_required
def tweet_react(request, tweet_id, *args, **kwargs):
    try:
        tweet = Tweet.objects.get(id=tweet_id)
    except:
        return JsonResponse({'message': "Tweet doesn't exist anymore!"})
    react = request.POST.get('react')
    
    if react == 'like':

    # user didn't react to tweet before
        if request.user not in tweet.likes.all() and request.user not in tweet.dislikes.all():
            tweet.likes.add(request.user)
            return JsonResponse({
                "likes": tweet.likes.count(),
                "dislikes": tweet.dislikes.count(),
                'like': 'add',
                'dislike': 'remove'
            })

        elif request.user in tweet.likes.all():
            tweet.likes.remove(request.user)
            return JsonResponse({
                "likes": tweet.likes.count(),
                "dislikes": tweet.dislikes.count(),
                'like': 'remove',
                'dislike': 'remove'
            })

        elif request.user in tweet.dislikes.all():
            tweet.dislikes.remove(request.user)
            tweet.likes.add(request.user)
            return JsonResponse({
                "likes": tweet.likes.count(),
                "dislikes": tweet.dislikes.count(),
                'like': 'add',
                'dislike': 'remove'
            })

    elif react == 'dislike':

        # user didn't react to tweet before
        if request.user not in tweet.likes.all() and request.user not in tweet.dislikes.all():
            tweet.dislikes.add(request.user)
            return JsonResponse({
                "likes": tweet.likes.count(),
                "dislikes": tweet.dislikes.count(),
                'like': 'remove',
                'dislike': 'add'
            })

        elif request.user in tweet.dislikes.all():
            tweet.dislikes.remove(request.user)
            return JsonResponse({
                "likes": tweet.likes.count(),
                "dislikes": tweet.dislikes.count(),
                'like': 'remove',
                'dislike': 'remove'
            })

        elif request.user in tweet.likes.all():
            tweet.dislikes.add(request.user)
            tweet.likes.remove(request.user)
            return JsonResponse({
                "likes": tweet.likes.count(),
                "dislikes": tweet.dislikes.count(),
                'like': 'remove',
                'dislike': 'add'
            })


from .serializers import TweetSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication

# restrict other views like GET & can't use Response without it
# we can modify API to accept ['DELETE', 'GET', 'POST']
@api_view(['POST']) 

# Those authentications decorators can be set at CBV & settings.py
# Allow just authenticated user to create tweet through API
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated]) 

# Login will not be changed, normal function just the reponse will be changed.
def tweet_create_drf(request, *args, **kwargs):
    serializer = TweetSerializer(data=request.POST)
    if serializer.is_valid():
        obj = serializer.save(author=request.user)
        return Response({"process": "success", "tweet": serializer.data})
    return Response({"process": "failed", "errors": serializer.errors})