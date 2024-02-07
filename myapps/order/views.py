from django.shortcuts import render
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.generic import ListView, View, CreateView, TemplateView, FormView, UpdateView
from ..product.models import  Detail
from django.contrib.contenttypes.models import ContentType
from ..member.models import *
# Create your views he
# cart/views.py
from rest_framework.generics import ListAPIView, CreateAPIView
from .models import Order,ProductOrder
from ..core.models import Image
from .serializers import *
import json
class ProfileApiView(APIView):
   serializer_class = OrderSerializer
   def get(self, request):
        user = self.request.user.id
        user_obj=CustomUser.objects.filter(id=user)
        address=UserAddress.objects.filter(user_id=user_obj.first())
        cities=City.objects.all()
        provinces=Province.objects.all()
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
        user_serializer=CustomerUserSerializer(user_obj,many=True)
        address_serializer=AddressSerializer(address,many=True)
        city_serializer=CitySerializer(cities,many=True)
        province_serializer=ProvinceSerializer(provinces,many=True)

        response_data = {
            'orders': order_serializer.data,
            'products': product_serializer.data,
            'images':image_serializer.data,
            'user':user_serializer.data,
            'addresses':address_serializer.data,
            'city':city_serializer.data,
            'provinces':province_serializer.data


        }
        # print("k"*50,order_serializer.data)
        # print("k" * 50, response_data)
        return Response( response_data)

class ProfileView(TemplateView):
    template_name = 'order/prof.html'


class CreateAddressView(APIView):
    # serializer_class = OrderSerializer

    def post(self, request):
        city_name=request.data.get('city')
        province_name=request.data.get('province')
        description=request.data.get('description')
        province_obj=Province.objects.get(name=province_name)
        city_obj=City.objects.get(name=city_name,province_id=province_obj)
        UserAddress(city=city_obj,description=description,user_id=request.user).save()
        return Response({"status":"success","message":"your addres save successfully"})

class UpdateUserView(APIView):
    def post(self, request):
        user_obj=request.user

        serializer = CustomerUserSerializer(user_obj, data=request.data,partial=True)
        if serializer.is_valid():

                serializer.save()
                return Response({"status": "success", "message": "update success"})


        else:
            return Response({"status":"fail","message":"fail to update"})


class CartView(APIView):
    def get(self,request):
        return render(request,'order/cart.html')

    def post(self,request):
        # info=request.data
        # print(type(info))
        if request.data:
            for id,count in request.data.items():
                product=Product.objects.get(id=id)


        return Response({"status":"success","message":"your addres save successfully"})


class CheckCodeView(APIView):
    def post(self,request):
        # check code and save to postgresqll
        return Response({"status":"success","message":"your code save successfully","value":200,"id_code":1})

        return Response({"status": "fail", "message": "code not found"})
class CreateCartView(View):
    def post(self,request):
        cart=request.data.get("cart")
        code=request.data.get("code")

        code_value=55#get from redis and save in postgresql
        id_code=2#get from postgresql




        # Order(discount_code_id=id_code,creator=request.user,final_payment=float(payment)-float(code_value)).save()