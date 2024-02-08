from datetime import timedelta

from django.core.cache import cache
from django.shortcuts import render
from django.utils import timezone
from django.views.generic import ListView, View, CreateView, TemplateView, FormView, UpdateView
# Create your views here.
from ..product.models import *
class Index(View):
    def get(self, request):
            context={}
            # for cat in Category.objects.all():
            #     if cat.childrn() != None:
            #         cache.set(cat.title, cat.childrn())

            five_days_ago = timezone.now() - timedelta(days=5)
            context['new_products'] =Product.objects.filter(created_at__gte=five_days_ago)
            context['cheapest']=Detail.objects.filter(name='cost').order_by('value')[:30]
            

            # print("c"*50,cache._cache.keys())
            return render(request,"core/index.html",context)


