from django.db import models

from django.contrib.auth.models import User

# Import PIL to manipulate image files
from PIL import Image

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):

    def create_user(self, email, username, gender, first_name, last_name, password=None):
        """
        Creates and saves a User with the given email, username, gender
        and password.
        """
        if not email:
            raise ValueError("Users must have Email")
        if not username:
            raise ValueError("Users must have username")

        user = self.model(

            # lowercase the domain portion of the email address
            email = self.normalize_email(email),
            username = username,
            gender = gender,
            first_name = first_name,
            last_name = last_name 
        )

        #This function will hash given password from NewUser
        user.set_password(password)

        user.save(using=self._db)

        return user

    def create_superuser(self, email, username, gender, first_name, last_name, password):
        """
        Creates and saves a superuser with the given email, username and password.
        """
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password,
            gender = gender,
            first_name = first_name,
            last_name = last_name
        )

        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class NewUser(AbstractBaseUser, PermissionsMixin):
    """
        New User model after modification
    """

    #Gender choices, values that will be displayed to user.
    GENDER_CHOICES = (
        (1, 'Male'),
        (2, 'Female'),
    )    

    # Any Field that you want to add or modify to your user Email
    email           = models.EmailField(max_length=60, unique=True)
    username        = models.CharField(max_length=10, unique=True)
    gender          = models.IntegerField(choices=GENDER_CHOICES)
    first_name      = models.CharField(max_length=10, unique=False)
    last_name       = models.CharField(max_length=10, unique=False)
    image           = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    bio             = models.TextField(max_length=250, blank=True, null=True)
    following       = models.ManyToManyField("self", related_name="followed_by", symmetrical=False)   

    # Those Fields are Required with AbstractBaseUser to work as expected.
    date_joined     = models.DateTimeField(auto_now_add=True)
    is_admin        = models.BooleanField(default=False)
    is_active       = models.BooleanField(default=True)
    is_staff        = models.BooleanField(default=False)
    is_superuser    = models.BooleanField(default=False)
    # password field supplied by AbstractBaseUser
    # last_login field supplied by AbstractBaseUser
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'gender', 'first_name', 'last_name']

    def __str__(self):
        return f"{self.email}"

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return self.is_admin
    
    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True

    def save(self, *args, **kwargs):

        # Ensure that it is the first time to add image and creat User
        if not self.image:
            if self.gender == 1:
                self.image = 'male.jpg'
            elif self.gender == 2:
                self.image = 'female.jpg'
            return super(NewUser, self).save(*args, **kwargs)
        return super(NewUser, self).save(*args, **kwargs)