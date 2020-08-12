from django.contrib import admin
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.admin import UserAdmin

from users.models import NewUser


# Register your models here.
class AddUserForm(forms.ModelForm):
    """
        New User Form, requires password configuration
    """
    password1 = forms.CharField(
        label='Password', widget=forms.PasswordInput
    )

    password2 = forms.CharField(
        label='Confirm password', widget=forms.PasswordInput
    )

    class Meta:
        model: UserAdmin

    def clean_password2(self):
        # check that 2 passwords entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Password don't match")
        return password2

class NewUserAdmin(UserAdmin):
    add_form = AddUserForm

    list_display = ('email', 'username', 'is_admin', 'is_staff', 'date_joined')
    search_fields = ('email', 'username')
    readonly_fields = ('date_joined', 'last_login')

    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('personal info', {'fields': ('first_name', 'last_name', 'gender', 'image', 'bio')}),
        ('permessions', {'fields': ('is_active', 'is_admin', 'is_superuser')}),
        ('time', {'fields': ('date_joined', 'last_login')})
    )



    add_fieldsets = (
        (None, {
            'fields': ('email', 'password1', 'password2', 'username', 'gender', 'first_name', 'last_name')
        }),
    )

admin.site.register(NewUser, NewUserAdmin)