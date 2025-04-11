from django.contrib import admin

from authentication.models import User
from .models import Profile, Training

# Register your models here.
admin.site.register(Profile)
admin.site.register(Training)

class CustomUserCreationForm():

    class Meta:
        model = User
        fields = '__all__'


class CustomUserChangeForm():

    class Meta:
        model = User
        fields = '__all__'