from django.urls import path
from . import views

app_name = 'product'
urlpatterns = [
    path('category/', views.CategoryView.as_view(), name='category'),
]