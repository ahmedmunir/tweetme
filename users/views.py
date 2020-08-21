from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import Http404, JsonResponse
from django.contrib.auth.decorators import login_required

from users.forms import UserRegisterForm
from users.models import NewUser
from tweets.models import Tweet

from users.forms import UserUpdateForm
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
        selected_user = NewUser.objects.filter(username=username).first()
    except:
        raise Http404
    
    if not selected_user:
        raise Http404
    
    return render(request, 'users/user_profile.html', {"selected_user": selected_user})

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
    # The Client side has start variable which define the last item we search for at DB
    quantity = 10
    start = int(request.GET.get('start'))
    last_index = Tweet.objects.last().pk
    end_range = last_index - start
    start_range = end_range - quantity

    # Queryset depending on User then depending on range
    query_set = list(Tweet.objects.filter(author=user).filter(id__range=(start_range, end_range)).order_by("-date_posted"))

    # Ensure that 10 data set will be returned to client side.
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

# Follow
@login_required
def user_follow(request, *args, **kwargs):

    
    if request.method == "POST":
        state  = request.POST.get('state')
        target = request.POST.get('target')

        try:
            target_user    = NewUser.objects.filter(username=target).first()
        except:
            return JsonResponse({
                "state": "can't Follow or unfollow now"
            })

        # Ensure that no one will try to follow himself
        if request.user != target_user:
            # If the process is Follow
            if state == 'Follow':

                request.user.following.add(target_user)
                request.user.save()
                return JsonResponse({
                    "state": "follow"
                }) 

            # If the procss is unfollow
            elif state == 'Unfollow':
                request.user.following.remove(target_user)
                request.user.save()
                return JsonResponse({
                    "state": "unfollow"
                })
            else:
                return JsonResponse({
                    "state": "You need to Login First"
                })

# Following Function
def user_following(request, username, *args, **kwargs):
    try:
        user_following = NewUser.objects.filter(username=username).first()
    except:
        raise Http404
    if not user_following:
        raise Http404

    return render(request, "users/user_following.html", {"user_following": user_following})

# Followers Function
def user_followers(request, username, *args, **kwargs):
    try:
        user_followers = NewUser.objects.filter(username=username).first()
    except:
        raise Http404
    if not user_followers:
        raise Http404

    return render(request, "users/user_followers.html", {"user_followers": user_followers})

# User Profile Edit
@login_required
def user_profile(request, *args, **kwargs):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, request.FILES, instance=request.user)

        if u_form.is_valid():
            
            # Delete old image first
            if 'profile_pics' in NewUser.objects.filter(id=request.user.id).first().image.url and request.FILES:
                NewUser.objects.filter(id=request.user.id).first().image.delete(False)
            
            u_form.save()
            messages.success(request, 'Your data updated successfully!')
            return redirect('edit_profile')
        else:
            return render(request, 'users/edit_profile.html', {"u_form": u_form})
    else:
        u_form = UserUpdateForm(instance=request.user)
        return render(request, 'users/edit_profile.html', {"u_form": u_form})