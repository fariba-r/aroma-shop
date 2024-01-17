from django.db import models
from ..product.models import Status,Product
from ..member.models import Staff,CustomUser
from django.core.exceptions import ValidationError
# Create your models here.
class ValidationMixin():
    @staticmethod
    def validate_payment(value):
        if value<0:
            raise ValidationError('the value should be positive')

class DiscountCodeUsed(models.Model,ValidationMixin):
    creator = models.ForeignKey(Staff,on_delete=models.PROTECT)
    created_at = models.DateTimeField()
    date_used = models.DateTimeField(auto_now=True)
    value=models.FloatField(validators=[ValidationMixin.validate_payment])

    


    
class Order(Status,ValidationMixin):
    product_id= models.ManyToManyField(Product, through='ProductOrder', related_name='order')
    discount_code_id = models.OneToOneField(DiscountCodeUsed,null=True,blank=True, related_name='orderr',on_delete=models.PROTECT)
    final_payment = models.FloatField(validators=[ValidationMixin.validate_payment])
    
    # Use the choices argument to specify the possible values for the status column
    STATUS_CHOICES = [
        ('P', 'Pending'),
        ('D', 'Delivered'),
        ('C', 'Confirmed'),
    ]
    pyment_status = models.CharField(max_length=1, choices=STATUS_CHOICES)
   
class ProductOrder(models.Model):
    product_id=models.ForeignKey(Product,on_delete=models.CASCADE)
    order_id=models.ForeignKey(Order,on_delete=models.CASCADE)
    count=models.PositiveIntegerField()