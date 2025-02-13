from django.contrib import admin
from django.urls import path
from myapp import views
from myapp.models import Profile
from myapp.views import profile_info, profile_create_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('profile/<str:first_name>/', views.profile_info, name='profile_info'),
    path('create/', profile_create_view, name='profile_create'),
]


