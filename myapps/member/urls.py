from django.urls import path
from . import views
from django.urls import reverse, reverse_lazy

from django.contrib.auth.views import LogoutView 

app_name = 'member'
urlpatterns = [
    path('login/', views.LoginPassView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('core:home')),name='logout'),
    path('singup/', views.SignUpView.as_view(), name='signup'),

]