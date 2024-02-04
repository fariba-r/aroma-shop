from django.urls import path
from . import views

app_name = 'order'
urlpatterns = [
     path('profile_drf/', views.ProfileApiView.as_view(), name='profile_drf'),
     path('profile/', views.ProfileView.as_view(), name='profile'),
]