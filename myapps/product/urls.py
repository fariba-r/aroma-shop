from django.urls import path
from . import views

app_name = 'account'
urlpatterns = [
<<<<<<< Updated upstream
    # path('staff_sign_up/', views.StaffSignUpView.as_view(), name='Staff_signup'),
=======
    path('category/', views.CategoryView.as_view(), name='category'),
path('products/<int:id>/', views.product_view, name='products'),

<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
]