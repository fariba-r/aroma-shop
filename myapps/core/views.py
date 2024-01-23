from django.shortcuts import render
from django.views.generic import ListView, View, CreateView, TemplateView, FormView, UpdateView
# Create your views here.

class Index(TemplateView):
    template_name="base.html"


