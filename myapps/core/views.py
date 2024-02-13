from datetime import timedelta
from django.core.cache import cache
from django.db.models import Count
from django.shortcuts import render
from django.utils import timezone
from django.views.generic import ListView, View, CreateView, TemplateView, FormView, UpdateView
# Create your views here.
from ..product.models import *
from ..core.models import *
from django.core.paginator import Paginator
from django.core.cache import cache
class Index(View):
    paginate_by = 2
    def get(self, request):
        cache.clear()
        five_days_ago = timezone.now() - timedelta(days=5)
        newest = Product.objects.filter(created_at__gte=five_days_ago) # Replace with your actual queryset
        items_per_page = 2
        paginator = Paginator(newest, items_per_page)
        page_number = request.GET.get('page', 1)

        # Get the Page object for the current page
        page = paginator.get_page(page_number)

        # Pass the Page object to the template context
        context = {'newest': page}
        # context={}
            # for cat in Category.objects.all():
            #     if cat.childrn() != None:
            #         cache.set(cat.title, cat.childrn())
        most_like=Product.objects.prefetch_related('')
        best_like = Like.objects.annotate(num_likes=Count("object_id")).filter(content_type=ContentType.objects.get_for_model(Detail)).order_by('-num_likes')[:3]
         # for item in best_like:


         # context["best"]=
        context['cheapest']=Detail.objects.filter(name='cost').order_by('value')[:30]
        context["categories"]=Category.objects.filter(parent=None)

        cache.set('categories', Category.objects.filter(parent=None))
            # print("c"*50,cache._cache.keys())
        return render(request,"base.html",context)


