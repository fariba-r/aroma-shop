from django.shortcuts import render
<<<<<<< Updated upstream

# Create your views here.
=======
from django.views.generic import ListView, View, CreateView, TemplateView, FormView, UpdateView
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.contrib.contenttypes.models import ContentType
from .models import *
from ..core.models import Image
# Create your views here.
class CategoryView(View):
    def get(self, request, *args, **kwargs):

        all_category = Category.objects.all()
        images=Image.objects.filter(content_type=ContentType.objects.get_for_model(Category))
        context={
            'all_category': all_category,
            'images': images
        }
        return render(request, 'product/category.html', context)


def product_view(request,id):
    if request.method == 'GET':
        category=Category.objects.get(id=id)
        products=category.get_products_recursively()
        images = Image.objects.filter(content_type=ContentType.objects.get_for_model(Product))
        context={
           " products":products,
            "images":images
        }
        return render(request, 'products.html',context)
>>>>>>> Stashed changes
