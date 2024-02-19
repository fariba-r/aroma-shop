
from urllib import request
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render, redirect
import requests
from django.views.generic import ListView, View, CreateView, TemplateView, FormView, UpdateView, DetailView

from django.shortcuts import render
from django.views.generic import ListView, View, CreateView, TemplateView, FormView, UpdateView

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
        bgd=Detail.objects.filter(Q(detaill__in=products_id),dependency=None)
        # cost=Detail.objects.filter(name="cost",dependency=bgd.first())
        cost = Detail.objects.filter( Q(detaill__in=products_id),name="cost")
        # n_cat=Category.objects.filter(parent=category)
        images = Image.objects.filter(content_type=ContentType.objects.get_for_model(Detail))
        context={
           "qs_products":qs_products,
            "cost":cost,
            "images":images
        }
        # print(context)
        return render(request, 'product/products.html',context)

class SingleProduct(DetailView):
    model = Product
    template_name = 'product/single_product.html'
    context_object_name="product"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object=Product.objects.get(id=self.kwargs['pk'])
        detail=Detail.objects.filter(detaill=self.kwargs["pk"])
        base_g=object.base_group
        images=Image.objects.filter(content_type=ContentType.objects.get_for_model(Detail),object_id=base_g.first().id )
        context['images'] = images
        context["details"]=detail
        context["categories"]=object.all_categoryes()
        context["example"]=base_g.first()
        context["comments"]=Comment.objects.filter(item_id=self.kwargs['pk'],is_ok=True)
        context["discount"]=DicountPercent.objects.filter(detail_id=base_g.first())


        # sesion
        # session = requests.Session()
        # for bg in base_g:
        #     self.request.session['idempresa'] = "mm"
            # requests.session[f"{bg.id}"] =bg
        return context

# class SingleProduct(View):
#     def get(self, request, *args, **kwargs):
#         objs=Product.objects.get(id=self.kwargs['pk'])
#
#         context={
#             "product":Product.objects.filter(product=objs.product)
#         }

class CreateComment(PermissionRequiredMixin,View,LoginRequiredMixin):
    permission_required = "add_comment"
    def handle_no_permission(self):
        messages.warning(request, "you should login first .")
        return redirect(render(reverse("member:login")))
    def post(self,request,id):

        product = Product.objects.get(id=id)
        comment=request.POST.get('comment')
        Comment.objects.create(content=comment,creator=self.request.user,item_id=product)
        return redirect(reverse("product:single_product",  args=(product.id,)))

class CreateReplyComment( LoginRequiredMixin,View):

        def handle_no_permission(self):
            messages.warning(request, "you should be staff to can reply .")
            return redirect(render(reverse("member:login")))

        def post(self, request, id_p,id_c):
            product = Product.objects.get(id=id_p)
            comment=Comment.objects.get(id=id_c)
            content = request.POST.get('comment')
            Comment.objects.create(content=content, creator=self.request.user, item_id=product,parent=comment)
            messages.warning(request, "reply save succes fully .")
            return redirect(reverse("product:single_product",  args=(id_p,)))
