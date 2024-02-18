from django.urls import path
from . import views
from django.urls import reverse, reverse_lazy

from django.contrib.auth.views import LogoutView


app_name = 'member'
urlpatterns = [
    path('loginpass/', views.LoginPassView.as_view(), name='loginpass'),
    path('loginpassapi/', views.LoginPassAPIView.as_view(), name='loginpassapi'),
    path('loginemail/', views.LoginEmailView.as_view(), name='loginemail'),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('core:index')), name='logout'),
    path('singup/', views.SignUpView.as_view(), name='signup'),
    path('check_email/', views.ValidateEmailView.as_view(), name='check_email'),
    path('check_code/', views.ValidateCodeView.as_view(), name='check_code'),
    path('activate_acount/',views.ActivateAPIView.as_view(),name='activate')

#     reset password-------

]
