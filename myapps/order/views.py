import datetime
from linecache import cache

from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.generic import ListView, View, CreateView, TemplateView, FormView, UpdateView
from ..product.models import  Detail
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
   # authentication_classes = [SessionAuthentication, BasicAuthentication]
   serializer_class = OrderSerializer
   # permission_classes = [IsAuthenticated]

   def get(self, request):
        if token := request.COOKIES.get('jwt'):
            print(token)
            try:
                # payload = jwt.decode(token, 'secret', algorithms=['HS256'])
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
                user = get_user_model().objects.filter(id=payload.get('id')).first() or \
                       get_user_model().objects.filter(id=payload.get('user_id')).first()
            except Exception as e:
                print('error: ', e)

        user_obj=CustomUser.objects.filter(id=user.id)
        address=UserAddress.objects.filter(user_id=user_obj.first())
        cities=City.objects.all()
        provinces=Province.objects.all()

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
    serializer_class=CustomerUserSerializer
    permission_classes = [IsAuthenticated]
    def put(self, request):
        user_obj=request.user
        print(user_obj)

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
        code_front=request.data["code"]
        condition = request.data["cost"]
        code_db=DiscountCode.objects.filter(code=code_front,owner=request.user.id,date_used=None)
        if code_db and code_db.date_expiered>= datetime.datetime.now:
            if code_db.condition<=condition:
                return Response({"status": "success", "message": "your code save successfully", "value": code_db.value, "id_code":code_db.code})

            else:
                return Response({"status": "fail", "message": f"you should buy {code_db.value } till code active."})
        else:
            return Response({"status": "fail", "message": "code not found"})

class CreateCartView(APIView):
    def post(self,request):

        code=request.data.get("code")
        try:
            if code:

                code_db=DiscountCode.objects.get(code=code)
                if not (code_db.date_expiered >= datetime.datetime.now() ):
                    raise ValueError

                code_db.date_used=datetime.datetime.now()
                code_db.save()
                cart=json.loads(request.data.get("cart"))

                Order.objects.create(discount_code_id=code,pyment_status=cart["status"],final_payment=0,creator=request.user).save()
                id_order= Order.objects.filter(creator=request.user).order_by("-asc").first()
                payment=0
                for k ,v in cart.items():
                    product=Product.objects.get(id=int(k))
                    count=v["count"]
                    cost=Detail.objects.get(product=product,name="cost").value
                    payment+=int(count)*float(cost)
                    ProductOrder(count=count,order_id=id_order,product_id=product).save()
                payment=payment-float(code.value)
                id_order.final_payment=payment
                id_order.save()
            else:
                cart = json.loads(request.data.get("cart"))

                Order.objects.create(discount_code_id=code, pyment_status=cart["status"], final_payment=0,
                                     creator=request.user).save()
                id_order = Order.objects.filter(creator=request.user).order_by("-asc").first()
                payment = 0
                for k, v in cart.items():
                    product = Product.objects.get(id=int(k))
                    count = v["count"]
                    cost = Detail.objects.get(product=product, name="cost").value
                    payment += int(count) * float(cost)
                    ProductOrder(count=count, order_id=id_order, product_id=product).save()

                id_order.final_payment = payment
                id_order.save()




            return Response({"status": "success"})
        except:
            return Response({"status": "fail"})


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


class CheckStoreView(APIView,ChangeStoreMixin):
    def post(self, request):
        cart = json.loads(request.data.get("cart"))
        try:
            ChangeStoreMixin.change(self,"-" ,cart)



            return Response({"status": "success"})
        except Exception as e:
            return Response({"status": "fail","message": str(e)})

class BackStoreView(APIView,ChangeStoreMixin):
    """
    .description:

        wrbfuhwuerr

    .input:

        salam

    .output:

        goodbuy



    """
    # permission_classes = []
    serializer_class = OrderSerializer

    def post(self, request):
        # todo:  serializerrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr

        cart = json.loads(request.data.get("cart"))
        ChangeStoreMixin.change(self, "+", cart)
        return Response({"status": "success"})

class ShowAddressView(APIView):
    def get(self, request):
        address = UserAddress.objects.filter(user_id=request.user)
        address_serializer = AddressSerializer(address, many=True)
        response={'addresses':address_serializer.data}
        return Response(response)



