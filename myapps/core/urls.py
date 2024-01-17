from django.urls import path
from . import views

app_name = 'account'
urlpatterns = [
    path('home/', views.Index.as_view(), name='home'),
]