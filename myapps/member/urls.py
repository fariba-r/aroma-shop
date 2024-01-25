from django.urls import path
from . import views
from django.urls import reverse, reverse_lazy

from django.contrib.auth.views import LogoutView 

app_name = 'member'
urlpatterns = [
    path('loginpass/', views.LoginPassView.as_view(), name='loginpass'),
    path('loginemail/', views.LoginEmailView.as_view(), name='loginemail'),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('core:home')),name='logout'),
    path('singup/', views.SignUpView.as_view(), name='signup'),

]