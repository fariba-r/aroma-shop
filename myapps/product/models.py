from django.db import models
from ..member.models import CustomUser
from django.core.exceptions import ValidationError
# Create your models here.
from django.db import models
class Status(models.Model):
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='%(class)s')

    class Meta:
        abstract = True

# class Category(Status):
#     title = models.CharField(max_length=50)
#     parent = models.ForeignKey('self',null=True,blank=True,on_delete=models.CASCADE)
    
class Detail(Status):
    title = models.CharField(max_length=50,unique=True)
    parent = models.ForeignKey('self',null=True,blank=True,on_delete=models.CASCADE,related_name='detail')
    

class Product(Status):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    detail_id =  models.ManyToManyField(Detail)
    count = models.PositiveIntegerField()
    price = models.FloatField()
    
    def clean_price(self):
        if not 0<self.price<10000:
            raise ValidationError("Price must be positive and smaller than 10000")
        return True

class Comment(Status):
    content=models.TextField(max_length=600)
    is_ok=models.BooleanField(default=False)
    parent=models.ForeignKey("self",on_delete=models.SET("replyed to a deleted comment"),null=True,blank=True)
    item_id=models.ForeignKey(Product,on_delete=models.CASCADE)

class Dicount_percent(Status):
    expiration=models.DateTimeField()
    percent=models.FloatField(default=0.0)
    product_id=models.ManyToManyField(Product)
    
    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(percent__gt=0), name="positive_percent"
            ),
        ]

