from django.core.cache import cache
from django.shortcuts import render
from django.views.generic import ListView, View, CreateView, TemplateView, FormView, UpdateView
# Create your views here.
from ..product.models import *
class Index(View):
    def get(self, request):
        def get_context_data(self, **kwargs):

            context = super().get_context_data(**kwargs)
            for cat in Category.objects.all:
                cache.set(cat.title, cat.childrn())
            context['new_products'] =Po




