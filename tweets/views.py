from django.shortcuts import render
from django.http import HttpResponse, Http404, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from tweets.forms import TweetForm
from tweets.models import Tweet
# Create your views here.

# Home Function
def home_view(request, *args, **kwargs):
    form = TweetForm()
    return render(request, "pages/home.html", context={"form": form}, status=200)

# Create Tweet
def tweet_create(request, *args, **kwargs):
    form = TweetForm(request.POST)
    if form.is_valid():
        new_tweet = form.save()
        return JsonResponse({"process": "success", "tweet": new_tweet.serialize()})
    return JsonResponse({"process": "failed", "errors": form.errors})
    

# List all Tweets
def tweet_list_view(request, *args, **kwargs):
    """
        REST API View for all Tweets
    """
    
    # Calculate the range of queryset according to user request 
    start = request.GET.get('start')
    end = request.GET.get('end')
    count = Tweet.objects.count()

    """
        Query data according to start & end request coming from User
        first_index_at_DB was added to solve the problem if there were data deleted
    """
    first_index_at_DB = Tweet.objects.first().pk
    start_range = count - int(start) + first_index_at_DB - 1 if count - int(start) > 0 else 0
    end_range = count - int(end) + first_index_at_DB - 1 if count - int(end)  > 0 else 0
    query_set = Tweet.objects.filter(id__range=(end_range, start_range)).order_by("-date_posted")

    # Convert tweets queryset into list to be able to send it through JSON
    tweets = [{"id": tweet.id, "content": tweet.content, "date_posted": tweet.date_posted} for tweet in query_set]
    data = {
        "isUser": False,
        "tweets": tweets,
    }
    return JsonResponse(data)

# Tweet detail view
def tweet_detail_view(request, tweet_id, *args, **kwargs):
    """
        REST API View for specific tweet 
    """
    data = {
        "id": tweet_id
    }
    try:
        tweet = Tweet.objects.get(id=tweet_id)
        data['content'] = tweet.content
        # data['image_path'] = tweet.image.url
        status = 200
    except:
        data['message'] = "Not Found"
        status = 404
    
    return JsonResponse(data, status=status)