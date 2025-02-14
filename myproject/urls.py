from django.contrib import admin
from django.urls import path, include
from myapp import views
from myapp.models import Profile
from myapp.views import profile_info, profile_create_view, profile_delete, profile_update, home_page

urlpatterns = [
    path('profile/<str:first_name>/', profile_info, name='profile_info'),
    path('create/', profile_create_view, name='profile_create'),
    path('update/<str:first_name>/', profile_update, name='profile_update'),
    path('delete/<str:first_name>/', profile_delete, name='profile_delete'),
    path('home_page', home_page, name='home_page'),

    # path('',include(myproject.urls))
]


