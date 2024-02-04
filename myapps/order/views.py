from django.shortcuts import render
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.generic import ListView, View, CreateView, TemplateView, FormView, UpdateView
from ..product.models import  Detail
from django.contrib.contenttypes.models import ContentType

# Create your views he
# cart/views.py
from rest_framework.generics import ListAPIView
from .models import Order,ProductOrder
from ..core.models import Image
from .serializers import OrderSerializer,ProductSerializer,ProductOrderSerializer,ImageSerializer

class ProfileApiView(APIView):
   serializer_class = OrderSerializer
   def get(self, request):
        user = self.request.user.id
        sessin=request.session.get('order')
        orders = Order.objects.filter(creator=user)
        list_order=[]
        for order in orders:
            list_order.append(order.id)

        order_product=ProductOrder.objects.filter(order_id__in=list_order)
        list_product = [op.product_id for op in order_product]
        list_bg=[]
        for p in list_product:
            for bg in p.base_group:
                list_bg.append(bg.id)
        # list_datail=[]
        #
        # for j in Detail.objects.filter(dependency__in=list_bg):
        #         list_datail.append(j.id)
        order_serializer = OrderSerializer(orders, many=True)
        product_serializer =ProductOrderSerializer(order_product, many=True)
        images=Image.objects.filter(object_id__in=list_bg,content_type=ContentType.objects.get_for_model(Detail))
        image_serializer=ImageSerializer(images,many=True)
        response_data = {
            'orders': order_serializer.data,
            'products': product_serializer.data,
            'images':image_serializer.data,
        }
        # print("k"*50,order_serializer.data)
        # print("k" * 50, response_data)
        return Response( response_data)

class ProfileView(TemplateView):
    template_name = 'order/prof.html'