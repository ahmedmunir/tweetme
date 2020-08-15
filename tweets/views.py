from django.shortcuts import render, redirect
from django.http import JsonResponse, Http404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ValidationError

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

# Retweet Tweet
@login_required
def tweet_retweet(request, tweet_id, *args, **kwargs):
    if request.method == "POST":
        try:
            tweet = Tweet.objects.filter(id=tweet_id).first()
        except:
            messages.warning(request, "Something went wrong with Server!")
            return redirect('home')
        
        # If tweet doesn't exist return error message
        if not tweet:
            messages.warning(request, "This tweet doesn't exist anymore!")
            return redirect('home')

        # Ensure that retweet will be for a Tweet not a retweet
        if tweet.retweet:
            messages.warning(request, "You can't make a retweet for a retweet")
            return redirect('home')

        # Ensure that user will not enter false Info
        try:
            rt = Tweet.objects.create(
                content=request.POST.get('content'),
                author=request.user,
                retweeted_tweet=tweet,
                retweet=True
            )
        except ValidationError as e:
            messages.warning(request, e)
            return redirect('home')

        rt.save()

        return redirect('home')

# Edit Tweet
@login_required
def tweet_edit(request, tweet_id, *args, **kwargs):
    try:
        tweet = Tweet.objects.filter(id=tweet_id).first()
    except:
        raise Http404
    
    # Ensure that the owner of tweet who wants to edit it
    if tweet.author != request.user:
        return JsonResponse({
            "message": "Error",
            "content": "You can't Edit the tweet while you are not the Owner"
        })
    
    # Ensure that there is a content sent by the user
    elif len(request.POST.get('content')) == 0:
        return JsonResponse({
            "message": "Error",
            "content": "You can't Post Empty Tweet"
        })

    print(request.POST.get('content'))
    tweet.content = request.POST.get('content')
    tweet.save()
    return JsonResponse({
        "message": "Done Editing",
        "content": tweet.content
    })
