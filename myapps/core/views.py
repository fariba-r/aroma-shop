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
from django.db.models import Subquery
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

        cheapest_detail=Detail.objects.filter(name='cost').order_by('value')[:30]

        best_like = Product.objects.filter(id__in=Like.objects.filter(content_type=ContentType.objects.get_for_model(Product)).values('object_id').annotate(num_likes=Count("object_id")).values("object_id"))
        # Like.objects.filter(content_type=ContentType.objects.get_for_model(Product)).values('object_id').annotate(num_likes=Count("object_id")).order_by("-num_likes")[:3]



         # context["best"]=
        context['cheapest']=cheapest_detail.values("detaill")
        context["categories"]=Category.objects.filter(parent=None)
        context["best_product"]=best_like
        context["images"]=Image.objects.filter(content_type=ContentType.objects.get_for_model(Detail))



        return render(request,"base.html",context)


