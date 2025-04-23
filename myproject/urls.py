from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect
from myapp import views

# Optionnel : redirection de la racine
def redirect_root(request):
    return redirect('/homepage')

urlpatterns = [
    # Profils
    path('me/', views.my_profile_view, name='my_profile'),
    path('create/', views.profile_create_view, name='profile_create'),
    path('<uuid:uuid>/', views.profile_info_view, name='profile_info'),
    path('update/<uuid:uuid>/', views.profile_update, name='profile_update'),
    path('delete/<uuid:uuid>/', views.profile_delete, name='profile_delete'),
    path('list/', views.profile_show, name='profile_show'),

    # Friend Requests
    path('friend-request/send/<uuid:uuid>/', views.send_friend_request, name='send_friend_request'),
    path('friend-request/accept/<int:pk>/', views.accept_friend_request, name='accept_friend_request'),
    path('friend-request/reject/<int:pk>/', views.reject_friend_request, name='reject_friend_request'),

    # Trainings
    path('training/<int:pk>/', views.training_info, name='training_info'),
    path('training/create/', views.training_create_view, name='training_create'),
    path('training/update/<int:pk>/', views.training_update, name='training_update'),
    path('training/delete/<int:pk>/', views.training_delete, name='training_delete'),
    path('trainings/', views.training_show, name='training_show'),

    # Calculators
    path('calculator/bmi/', views.bmi_view, name='bmi_calculator'),
    path('calculator/protein/', views.protein_view, name='protein_calculator'),
    path('calculator/calories/', views.calories_view, name='calories_calculator'),
    path('calculator/combined/', views.combined_view, name='combined_calculator'),

    # Auth
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Homepage
    path('', views.homepage, name='homepage'),
]
