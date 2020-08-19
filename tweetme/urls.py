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
from django.urls import include

from users import views as users_views

from tweets.views import home_view

from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', home_view, name="home"),

    path('favicon.ico/',
    RedirectView.as_view( # the redirecting function
        url=('/static/img/favicon.ico'), # converts the static directory + our favicon into a URL
    ),
    name="favicon" # name of our view
    ),

    # Tweets urls
    path('tweets/', include('tweets.urls')),

    # Password change & Reset URLS
    path('password-reset/',
    auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'),
    name='password_reset'),

    path('password-reset/done/',
    auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
    name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/',
    auth_views.PasswordResetConfirmView.as_view(template_name="users/password_reset_confirm.html"),
    name='password_reset_confirm'),

    path('password_change/',
    login_required(auth_views.PasswordChangeView.as_view(
        template_name='users/password_change.html'
    )), name='password_change'),

    path('password_change_done/',
    login_required(auth_views.PasswordChangeDoneView.as_view(
        template_name="users/password_change_done.html"
    )), name='password_change_done'),

    path('password-reset-complete/',
    auth_views.PasswordResetCompleteView.as_view(
        template_name='users/password_reset_complete.html'
        ),
    name='password_reset_complete'
    ),

    # User URLS (register, login, logout)
    path('profile/', users_views.user_profile, name="edit_profile"),
    path('follow/', users_views.user_follow, name='user-follow'),
    path('register/', users_views.register, name='register'),
    path('login/', users_views.loginCustom, name='login'),
    path('logout/', login_required(auth_views.LogoutView.as_view()), name='logout'),
    path('<str:username>/', users_views.profile, name='user-profile'),
    path('<str:username>/tweets/', users_views.user_tweets, name='user-tweets'),
    path('<str:username>/following/', users_views.user_following, name='user-following'),
    path('<str:username>/followers/', users_views.user_followers, name="user-followed_by"),
    

]

# Configure URLS for media files at development process
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
