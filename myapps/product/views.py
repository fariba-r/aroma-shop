from django.shortcuts import render

from django.views.generic import ListView, View, CreateView, TemplateView, FormView, UpdateView, DetailView
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.contrib.contenttypes.models import ContentType
from .models import *
from ..core.models import Image
# Create your views here.
class CategoryView(View):
    def get(self, request, *args, **kwargs):

        all_category = Category.objects.filter(parent=None)
        images=Image.objects.filter(content_type=ContentType.objects.get_for_model(Category))
        context={
            'all_category': all_category,
            'images': images
        }
        return render(request, 'product/category.html', context)


def products_view(request,id):
    if request.method == 'GET':
        category=Category.objects.get(id=id)
        products_id=category.get_products_recursively()
        qs_products=category.list_to_queryset(products_id)
        # n_cat=Category.objects.filter(parent=category)
        images = Image.objects.filter(content_type=ContentType.objects.get_for_model(Product))
        context={
           "qs_products":qs_products,

            "images":images
        }
        print(context)
        return render(request, 'product/products.html',context)

class SingleProduct(DetailView):
    model = Product
    template_name = 'product/single_product.html'
    context_object_name="product"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        images=Image.objects.filter(content_type=ContentType.objects.get_for_model(Product),object_id=self.kwargs['pk'])
        context['images'] = images
        context["categories"]=Product.objects.get(id=self.kwargs['pk']).all_categoryes()
        context["colors"]=Product.objects.get(id=self.kwargs['pk'])
        return context

# cclass SingleProduct(View):
#     def get(self, request, *args, **kwargs):
#         objs=Product.objects.get(id=self.kwargs['pk'])
#
#         context={
#             "product":Product.objects.filter(product=objs.product)
#         }
