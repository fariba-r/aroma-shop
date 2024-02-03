from django.urls import path
from . import views

app_name = 'order'
urlpatterns = [
     path('cart_drf/', views.CartApiView.as_view(), name='cart_drf'),
     path('cart/', views.CartView.as_view(), name='cart'),
]