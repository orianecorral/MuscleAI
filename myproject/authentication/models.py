from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser): 
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25, blank=True, null=True)
    username = models.CharField(max_length = 50, unique = True)
    email = models.EmailField(('email adress'), unique=True)
    password = models.CharField(max_length=255)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password']

    def __str__(self):
        return "{}".format(self.email)