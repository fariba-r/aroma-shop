from django.db import models
from ..product.models import Product
from ..member.models import Staff,CustomUser,Status,UserAddress
from django.core.exceptions import ValidationError
from ..core.manager import CustomBaseManager,DeleteMixin

# Create your models here.
class ValidationMixin():
    @staticmethod
    def validate_payment(value):
        if value<0:
            raise ValidationError('the value should be positive')

class DiscountCodeUsed(models.Model,DeleteMixin,ValidationMixin):
    creator = models.ForeignKey(Staff,on_delete=models.PROTECT)
    created_at = models.DateTimeField()
    date_used = models.DateTimeField(auto_now=True)
    value=models.FloatField(validators=[ValidationMixin.validate_payment])
    is_deleted = models.BooleanField(default=False)

    objects=CustomBaseManager()

    def __str__(self):
        return f"{self.value}"

    


    
class Order(Status):
    product_id= models.ManyToManyField(Product, through='ProductOrder', related_name='order')
    discount_code_id = models.OneToOneField(DiscountCodeUsed,null=True,blank=True, related_name='orderr',on_delete=models.PROTECT)
    final_payment = models.FloatField(validators=[ValidationMixin.validate_payment])
    
    # Use the choices argument to specify the possible values for the status column
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('InHome', 'InHome'),
        ('Delivered', 'Delivered'),
        ('Confirmed', 'Confirmed'),
    ]
    pyment_status = models.CharField(max_length=9, choices=STATUS_CHOICES)
    address_id = models.OneToOneField(UserAddress, related_name='address',on_delete=models.PROTECT)
    objects=CustomBaseManager()

    def __str__(self):
        return f" order {self.creator}"
   
class ProductOrder(models.Model,DeleteMixin):
    product_id=models.ForeignKey(Product,on_delete=models.CASCADE)
    order_id=models.ForeignKey(Order,on_delete=models.CASCADE)
    count=models.PositiveIntegerField()
    def __str__(self):
        return f" {self.product_id} {self.order_id}"
    # objects=CustomBaseManager()