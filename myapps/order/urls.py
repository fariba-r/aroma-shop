from django.urls import path
from . import views

app_name = 'order'
urlpatterns = [
     path('profile_drf/', views.ProfileApiView.as_view(), name='profile_drf'),
     path('profile/', views.ProfileView.as_view(), name='profile'),
     path('create_address/', views.CreateAddressView.as_view(), name='create_address'),
     path('cart/', views.CartView.as_view(), name='cart'),
     path('update_user/', views.UpdateUserView.as_view(), name='update_user'),
     path('check_code/', views.CheckCodeView.as_view(), name='check_code'),
     path('create_cart/', views.CreateCartView.as_view(), name='create_cart'),
]