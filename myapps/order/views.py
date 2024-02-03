from django.shortcuts import render
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.generic import ListView, View, CreateView, TemplateView, FormView, UpdateView


# Create your views he
# cart/views.py
from rest_framework.generics import ListAPIView
from .models import Order
from .serializers import OrderSerializer

class CartApiView(APIView):
   serializer_class = OrderSerializer
   def get(self, request):
        user = self.request.user.id
        orders = Order.objects.filter(creator=user)
        serializer = OrderSerializer(orders, many=True)
        print("k"*50,serializer.data)
        return Response( serializer.data)

class CartView(TemplateView):
    template_name = 'order/cart.html'