from django.shortcuts import render
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render

from tweets.models import Tweet
# Create your views here.

# Home Function
def home_view(request, *args, **kwargs):
    return render(request, "pages/home.html", context={}, status=200)


# Tweet detail view
def tweet_detail_view(request, tweet_id, *args, **kwargs):
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