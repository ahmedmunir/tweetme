from django import forms
from django.contrib.auth.forms import UserCreationForm

from users.models import NewUser

class UserRegisterForm(UserCreationForm):
    """
        Registeration Form
    """
    class Meta:
        model = NewUser
        fields = ['email', 'password1', 'password2', 'username', 'first_name', 'last_name', 'gender']


class UserUpdateForm(forms.ModelForm):
    """
        Update User data Form
    """

    class Meta:
        model = NewUser

        fields = ['username', 'email', 'gender', 'first_name', 'last_name', 'bio', 'image']