from django.urls import path
from . import views
from django.urls import reverse, reverse_lazy

from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views

app_name = 'member'
urlpatterns = [
    path('loginpass/', views.LoginPassView.as_view(), name='loginpass'),
    path('loginemail/', views.LoginEmailView.as_view(), name='loginemail'),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('core:index')), name='logout'),
    path('singup/', views.SignUpView.as_view(), name='signup'),
    path('check_email/', views.ValidateEmailView.as_view(), name='check_email'),
    path('check_code/', views.ValidateCodeView.as_view(), name='check_code'),
#     reset password-------
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),

]
