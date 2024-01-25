from django.shortcuts import render
from django.views.generic import ListView, View, CreateView, TemplateView, FormView, UpdateView
from django.shortcuts import get_object_or_404
from .models import *
# Create your views here.
class CategoryView(View):
    def get(self, request, *args, **kwargs):
        category = Detail.objects.get_object_or_404(title='category')
        all_category = Product.filter(detail_id=category)
        
