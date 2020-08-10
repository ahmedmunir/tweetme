from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login

from users.forms import UserRegisterForm

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