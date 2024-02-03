# cart/serializers.py
from rest_framework import serializers
from .models import Order
from ..product.models import  Product

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
        fields = '__all__'  # Include all fields from the Product model

class OrderSerializer(serializers.ModelSerializer):
    product_id=ProductSerializer(read_only=True)
    discount_code_id=DiscountCodeSerializer(read_only=True)
    class Meta:
        model = Order

        fields = '__all__'  # Include all fields from the Order model
