# cart/serializers.py
from rest_framework import serializers
from .models import Order
from ..product.models import  Product
from ..core.models import  Image
from ..member.models import  CustomUser
class DiscountCodeSerializer(serializers.Serializer):
    value = serializers.FloatField()

    # def create(self, validated_data):
    #     # Implement your custom create logic here
    #     # For example, create a DiscountCodeUsed instance with the validated data
    #     return DiscountCodeUsed.objects.create(**validated_data)
    #
    # def update(self, instance, validated_data):
    #     # Implement your custom update logic here
    #     # For example, update the value of an existing DiscountCodeUsed instance
    #     instance.value = validated_data.get('value', instance.value)
    #     instance.save()
    #     return instance
class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields =('title','description')

class OrderSerializer(serializers.ModelSerializer):
    discount_code_id=DiscountCodeSerializer(read_only=True)
    class Meta:
        model = Order
        fields = ('discount_code_id', 'pyment_status','final_payment','created_at')

class ProductOrderSerializer(serializers.Serializer):
    product_id = ProductSerializer(read_only=True)
    order_id = OrderSerializer(read_only=True)


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('image',)

class ProvinceSerializer(serializers.Serializer):
    name=serializers.CharField()


class CitySerializer(serializers.Serializer):
    province_id = ProvinceSerializer(read_only=True)
    name = serializers.CharField()

class CustomerUserSerializer(serializers.ModelSerializer):
    # first_name=serializers.CharField(allow_null=True)
    # last_name=serializers.CharField(allow_null=True)
    # created_at=serializers.DateTimeField(allow_null=True)
    # is_active=serializers.BooleanField()
    # email=serializers.EmailField(allow_null=True)
    # phonenumber=serializers.CharField(max_length=11)
    # username=serializers.CharField()
    class Meta:
        model = CustomUser
        fields = ('first_name','last_name','created_at','email','phonenumber','username','is_active')
        read_only_fields = ['is_active']




class AddressSerializer(serializers.Serializer):
    city=CitySerializer(read_only=True)
    description=serializers.CharField()

