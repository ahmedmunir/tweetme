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

def tweet_create(request, *args, **kwargs):
    form = TweetForm(request.POST)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('home'))
    return JsonResponse({"process": "failed"})
    

# List all Tweets
def tweet_list_view(request, *args, **kwargs):
    """
        REST API View for all Tweets
    """
    start = request.GET.get('start')
    end = request.GET.get('end')
    query_set = Tweet.objects.filter(id__range=(int(start), int(end)))
    # Convert tweets queryset into list to be able to send it through JSON
    tweets = [{"id": tweet.id, "content": tweet.content} for tweet in query_set]
    data = {
        "isUser": False,
        "tweets": tweets
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