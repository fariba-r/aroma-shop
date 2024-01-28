from django.urls import path
from . import views

app_name = 'product'
urlpatterns = [

    path('category/', views.CategoryView.as_view(), name='category'),
path('products/<int:id>/', views.products_view, name='products'),
path('single_product/<int:pk>/', views.SingleProduct.as_view(), name='single_product'),
    ]

