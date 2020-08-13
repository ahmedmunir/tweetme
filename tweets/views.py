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
        new_tweet_serializer = new_tweet.serializer(request.user) 
        return JsonResponse({"process": "success", "tweet": new_tweet_serializer})
    return JsonResponse({"process": "failed", "errors": form.errors})
    

# List all Tweets
def tweet_list_view(request, *args, **kwargs):
    """
        REST API View for all Tweets
    """
    
    # Calculate the range of queryset according to user request 
    quantity = 10
    start = int(request.GET.get('start'))
    last_index = Tweet.objects.last().pk
    end_range = last_index - start
    start_range = end_range - quantity
    query_set = list(Tweet.objects.filter(id__range=(start_range, end_range)).order_by("-date_posted"))

    if(len(query_set) < 10):
        start += quantity
        while(len(query_set) < 10 and start_range > 0):
            try:
                new_data = Tweet.objects.filter(id=start_range).first()
            except:
                new_data = []
            if(new_data):
                query_set.append(new_data)
            start_range -= 1
            start += 1
    else:
        start += quantity

    # Convert tweets queryset into list to be able to send it through JSON
    tweets = [ tweet.serializer(request.user) for tweet in query_set]
    data = {
        "tweets": tweets,
        'start': start
    }
    return JsonResponse(data)

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
    else:
        return JsonResponse({'message': 'This react is not allowed to our tweets!'})

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
