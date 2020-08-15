from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import Http404, JsonResponse

from users.forms import UserRegisterForm
from users.models import NewUser
from tweets.models import Tweet

# Create your views here.

# Register View
def register(request, *args, **kwargs):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your account created successfully, You can log in now')
            return redirect('login')
    else:
        if request.user.is_authenticated:
            return redirect('home')
        else:
            form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

# Login View
def loginCustom(request, *args, **kwargs):
    if request.method == "POST":
        user = authenticate(request, email=request.POST.get('email'), password=request.POST.get('password'))
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Email or password are incorrect')
            return redirect('login')
    else:
        if request.user.is_authenticated:
            return redirect('home')
    return render(request, 'users/login.html')


# User profile
def profile(request, username, *args, **kwargs):
    try:
        user = NewUser.objects.filter(username=username).first()
    except:
        raise Http404
    
    if not user:
        raise Http404

    return render(request, 'users/user_profile.html', {"user": user})

# List all Tweets
def user_tweets(request, username, *args, **kwargs):
    """
        REST API View for all Tweets created by User
    """
    try:
        user = NewUser.objects.filter(username=username).first()
    except:
        raise Http404
    if not user:
        raise Http404

    
    # Calculate the range of queryset according to user request 
    quantity = 10
    start = int(request.GET.get('start'))
    last_index = Tweet.objects.last().pk
    end_range = last_index - start
    start_range = end_range - quantity
    query_set = list(Tweet.objects.filter(author=user).filter(id__range=(start_range, end_range)).order_by("-date_posted"))

    if(len(query_set) < 10):
        start += quantity
        while(len(query_set) < 10 and start_range > 0):
            try:
                new_data = Tweet.objects.filter(author=user).filter(id=start_range).first()
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