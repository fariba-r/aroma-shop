from django.urls import path
from . import views

app_name = 'core'
urlpatterns = [
    path('home/', views.Index.as_view(), name='index'),
# path('index/', views.Index.as_view(), name='index'),
]