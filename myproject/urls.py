from django.contrib import admin
from django.urls import path, include
from myapp import views
from django.shortcuts import redirect
from myapp.models import Profile, Training
from myapp.views import accept_friend_request, add_training_to_profile, bmi_view, calories_view, combined_view, login_view, logout_view, profile_info, profile_create_view, profile_delete, profile_update, profile_show, homepage, protein_view, reject_friend_request, send_friend_request, training_create_view, training_delete, training_info, training_show, training_update

def redirect_root(request):
    return redirect('/homepage')

urlpatterns = [
    path('', redirect_root),

    # path profile
    path('profile/<int:pk>/', profile_info, name='profile_info'),
    path('create_profile/', profile_create_view, name='profile_create'),
    path('update/<int:pk>/', profile_update, name='profile_update'),
    path('delete/<int:pk>/', profile_delete, name='profile_delete'),
    path('homepage', homepage, name='homepage'),
    path('profiles', profile_show, name='profile_show'),

    # path training
    path('trainings/<int:pk>/', training_info, name='training_info'), 
    path('create_training/', training_create_view, name='training_create'),
    path('trainings/update/<int:pk>/', training_update, name='training_update'),
    path('trainings/delete/<int:pk>/', training_delete, name='training_delete'),
    path('trainings', training_show, name='training_show'),
    path('add-training/<int:training_id>/', add_training_to_profile, name='add_training_to_profile'),


    # path('',include(myproject.urls))
    path('bmi/', bmi_view, name='bmi'),
    path('protein/', protein_view, name='protein'),
    path('calories/', calories_view, name='calories'),
    path('calculs/', combined_view, name='combined'),


    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    path('profile/<int:pk>/add-friend/', send_friend_request, name='send_friend_request'),
    path('profile/<int:pk>/accept-friend/', accept_friend_request, name='accept_friend_request'),
    path('profile/<int:pk>/reject-friend/', reject_friend_request, name='reject_friend_request'),

    path('profile/uuid/<uuid:uuid>/', views.profile_by_uuid, name='profile_by_uuid'),

]


