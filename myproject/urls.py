from django.contrib import admin
from django.urls import path, include
from myapp import views
from django.shortcuts import redirect
from myapp.models import Profile, Training
from myapp.views import profile_info, profile_create_view, profile_delete, profile_update, profile_show, homepage, training_create_view, training_delete, training_info, training_show, training_update

def redirect_root(request):
    return redirect('/homepage')

urlpatterns = [
    path('', redirect_root),

    # path profile
    path('profile/<str:first_name>/', profile_info, name='profile_info'),
    path('create_profile/', profile_create_view, name='profile_create'),
    path('update/<str:first_name>/', profile_update, name='profile_update'),
    path('delete/<str:first_name>/', profile_delete, name='profile_delete'),
    path('homepage', homepage, name='homepage'),
    path('profiles', profile_show, name='profile_show'),

    # path training
    path('trainings/<int:pk>/', training_info, name='training_info'), 
    path('create_training/', training_create_view, name='training_create'),
    path('trainings/update/<int:pk>/', training_update, name='training_update'),
    path('trainings/delete/<int:pk>/', training_delete, name='training_delete'),
    path('trainings', training_show, name='training_show'),


    # path('',include(myproject.urls))
]


