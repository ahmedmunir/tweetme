"""tweetme URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from users import views as users_views

from tweets.views import (
    home_view,
    tweet_create,
    tweet_list_view,
    tweet_delete, 
    tweet_react,
    tweet_create_drf
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', home_view, name="home"),
    path('tweets/', tweet_list_view, name='tweets'),
    path('tweets/create/', tweet_create, name='tweet-create'),
    # path('tweets/create/', tweet_create_drf, name='tweet-create'),
    path('tweets/<int:tweet_id>/delete/', tweet_delete, name="tweet-delete"),
    path('tweets/<int:tweet_id>/react/', tweet_react, name='tweet-react'),

    # User URLS (register, login, logout)
    path('register/', users_views.register, name='register'),
    path('login/', users_views.loginCustom, name='login'),
    path('logout/', login_required(auth_views.LogoutView.as_view()), name='logout'),
    
    path('password-reset/',
    auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'),
    name='password-reset'),

    path('password-reset/done/',
    auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html')),

    path('password-reset-confirm/<uidb64>/<token>/',
    auth_views.PasswordResetConfirmView.as_view(template_name="users/password_reset_confirm.html")),

    path('password-change/',
    login_required(auth_views.PasswordChangeView.as_view(
        template_name='users/password_change.html'
    )), name='password-change'),

    path('password-change-done/',
    login_required(auth_views.PasswordChangeDoneView.as_view(
        template_name="users/password_change_done.html"
    )), name='password-change-done')



]

# Configure URLS for media files at development process
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
