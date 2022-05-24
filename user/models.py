import email
from django.db import models
# AbstractBaseUser
from django.contrib.auth.models import AbstractBaseUser

# Create your models here.

class User(AbstractBaseUser):
    # profile_image
    # user_id : nickname
    # user_email
    # user_password => default
    # name

    profile_image = models.TextField()
    user_id = models.CharField(max_length=24, unique=True)
    name = models.CharField(max_length=24)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'user_id'


    class Meta:
        db_table = 'user'

