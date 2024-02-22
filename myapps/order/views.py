import datetime
from linecache import cache

import pytz
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.generic import ListView, View, CreateView, TemplateView, FormView, UpdateView
from ..product.models import Detail
from django.contrib.contenttypes.models import ContentType
from ..member.models import *
# Create your views he

from rest_framework.generics import ListAPIView, CreateAPIView
from .models import Order, ProductOrder, DiscountCode
from ..core.models import Image
from .serializers import *
import json
import jwt
from jwt import exceptions

from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.authentication import SessionAuthentication, BasicAuthentication


class ProfileApiView(APIView):
    serializer_class = OrderSerializer
    def get(self, request):
        user_obj = CustomUser.objects.get(id=1)
        address = UserAddress.objects.filter(user_id=user_obj)
        cities = City.objects.all()
        provinces = Province.objects.all()
        orders = Order.objects.filter(creator=user_obj)
        list_order = []
        for order in orders:
            list_order.append(order.id)
        order_product = ProductOrder.objects.filter(order_id__in=list_order)
        list_product = [op.product_id for op in order_product]
        list_bg = []
        for p in list_product:
            for bg in p.base_group:
                list_bg.append(bg.id)
        # list_datail=[]
        #
        # for j in Detail.objects.filter(dependency__in=list_bg):
        #         list_datail.append(j.id)
        order_serializer = OrderSerializer(orders, many=True)
        product_serializer = ProductOrderSerializer(order_product, many=True)
        images = Image.objects.filter(object_id__in=list_bg, content_type=ContentType.objects.get_for_model(Detail))
        image_serializer = ImageSerializer(images, many=True)
        user_serializer = CustomerUserSerializer(user_obj)
        address_serializer = AddressSerializer(address, many=True)
        city_serializer = CitySerializer(cities, many=True)
        province_serializer = ProvinceSerializer(provinces, many=True)

        response_data = {
            'orders': order_serializer.data,
            'products': product_serializer.data,
            'images': image_serializer.data,
            'user': user_serializer.data,
            'addresses': address_serializer.data,
            'city': city_serializer.data,
            'provinces': province_serializer.data

        }

        return Response(response_data)


class ProfileView(TemplateView):
    template_name = 'order/prof.html'


class CreateAddressView(APIView):
    def post(self, request):
        city_name = request.data.get('city')
        province_name = request.data.get('province')
        description = request.data.get('description')
        province_obj = Province.objects.get(name=province_name)
        city_obj = City.objects.get(name=city_name, province_id=province_obj)
        UserAddress(city=city_obj, description=description, user_id=CustomUser.objects.get(id=1)).save()
        return Response({"status": "success", "message": "your addres save successfully"})


class UpdateUserView(APIView):
    serializer_class = CustomerUserSerializer
    # permission_classes = [IsAuthenticated]

    def put(self, request):
        user_obj = CustomUser.objects.get(id=1)
        serializer = CustomerUserSerializer(user_obj, data=request.data, partial=True)
        if serializer.is_valid():

            serializer.save()
            return Response({"status": "success", "message": "update success"},status=200)


        else:
            return Response({"status": "fail", "message": "fail to update"},status=500)


# class CartView(APIView):
#     def get(self, request):
#         return render(request, 'order/cart.html')

    # def post(self, request):
    #     # info=request.data
    #     # print(type(info))
    #     if request.data:
    #         for id, count in request.data.items():
    #             product = Product.objects.get(id=id)
    #
    #     return Response({"status": "success", "message": "your addres save successfully"})
class CartView(TemplateView):
    template_name = 'order/cart.html'


class CheckCodeView(APIView):
    def post(self, request):
        serializer = DiscoundCodeSerializer(data=request.data)
        if serializer.is_valid():
            code_front = serializer.validated_data["code"]
            condition = serializer.validated_data["cost"]
            code_db = DiscountCode.objects.filter(code=code_front, owner=CustomUser.objects.get(id=1), date_used=None)
            if code_db and code_db.first().date_expiered >= datetime.datetime.now(pytz.UTC):
                if code_db.first().condition <= float(condition):
                    return Response(
                        {"status": "success", "message": "your code save successfully", "value": code_db.first().value,
                         "id_code": code_db.first().code}, status=200)

                else:
                    return Response(
                        {"status": "fail", "message": f"you should buy {code_db.first().condition} till code active."},
                        status=200)
            else:
                return Response({"status": "fail", "message": "code not found"}, status=404)
        else:
            return Response({"status": "fail", "message": "somthing went wrong"}, status=500)


class CreateCartView(APIView):
    def post(self, request):

        code = request.data.get("code")
        try:
            if code:

                code_db = DiscountCode.objects.get(code=code,date_used =None)

                if not (code_db.date_expiered >= datetime.datetime.now(pytz.UTC)):
                    return Response({"status": "fail"},status=404)


                code_db.date_used = datetime.datetime.now(pytz.UTC)
                code_db.save()
                cart = json.loads(request.data.get("cart"))

                Order.objects.create(discount_code_id=code_db, pyment_status="Confirmed", final_payment=0,
                                     creator=CustomUser.objects.get(id=1),address_id=UserAddress.objects.get(id=1)).save()
                id_order = Order.objects.filter(creator=CustomUser.objects.get(id=1)).order_by("-created_at").first()
                payment = 0
                for k, v in cart.items():
                    product = Product.objects.get(id=int(k))
                    count = v["count"]
                    cost = Detail.objects.get(detaill=product, name="cost").value
                    payment += int(count) * float(cost)
                    ProductOrder(count=count, order_id=id_order, product_id=product).save()
                payment = payment - float(code_db.value)
                id_order.final_payment = payment
                id_order.save()
            else:
                cart = json.loads(request.data.get("cart"))


                Order.objects.create(pyment_status="Confirmed" ,final_payment=0,
                                     creator=CustomUser.objects.get(id=1),address_id=UserAddress.objects.get(id=1)).save()
                id_order = Order.objects.filter(creator=CustomUser.objects.get(id=1)).order_by("-created_at").first()
                payment = 0
                for k, v in cart.items():
                    product = Product.objects.get(id=int(k))
                    count = v["count"]
                    cost = Detail.objects.get(detaill=product, name="cost").value
                    payment += int(count) * float(cost)
                    ProductOrder(count=count, order_id=id_order, product_id=product).save()

                id_order.final_payment = payment
                id_order.save()

            return Response({"status": "success"},status=200)
        except Exception as e:
             print(e)
             return Response({"status": "fail"},status=500)


class ChangeStoreMixin:
    def change(self, operator, cart):
        for k, v in cart.items():
            product = Product.objects.get(id=int(k))
            count = v["count"]
            old_count = Detail.objects.get(detaill=product, name="count").value
            if operator == "-":
                new_count = int(old_count) - int(count)
            elif operator == "+":
                new_count = int(old_count) + int(count)
            if new_count > 0:
                obj = Detail.objects.get(detaill=product, name="count")
                obj.value = int(new_count)
                obj.save()
            else:
                raise ValueError(f"the count of {product.title} is {old_count}")


class CheckStoreView(APIView, ChangeStoreMixin):
    def post(self, request):
        cart = json.loads(request.data.get("cart"))
        try:
            ChangeStoreMixin.change(self, "-", cart)

            return Response({"status": "success"})
        except Exception as e:
            return Response({"status": "fail", "message": str(e)})


class BackStoreView(APIView, ChangeStoreMixin):
    """
    .description:

        wrbfuhwuerr

    .input:

        salam

    .output:

        goodbuy



    """
    # permission_classes = []
    # serializer_class = OrderSerializer

    def post(self, request):
        cart = json.loads(request.data.get("cart"))
        ChangeStoreMixin.change(self, "+", cart)
        return Response({"status": "success"})


class ShowAddressView(APIView):
    def get(self, request):

        address = UserAddress.objects.filter(user_id=CustomUser.objects.get(id=1))

        address_serializer = AddressSerializer(address, many=True)
        response = {'addresses': address_serializer.data}
        return Response(response)

# class DeleteAddresseView(APIView):
    def post(self,request):
        serializer=AddressSerializer(data=request.data)
        serializer.delete()
        return Response(status=200)
    def put(self,request):
        serializer=AddressSerializer(data=request.data)
        serializer.update()
        return Response(status=200)

