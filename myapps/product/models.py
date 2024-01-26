from django.db import models
from ..member.models import CustomUser
from django.core.exceptions import ValidationError
from django.db import models
from ..core.manager import CustomBaseManager
from ..member.models import Status


    
class Detail(Status):
    title = models.CharField(max_length=50,unique=True)
    parent = models.ForeignKey('self',null=True,blank=True,on_delete=models.CASCADE,related_name='detail')
    objects=CustomBaseManager()
    
class Category(Status):
    title = models.CharField(max_length=50, unique=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='detail')
    objects = CustomBaseManager()

    def get_products_recursively(self):
        products = []
        for category in self.__class__.objects.all():
            while (category.parent is not None):
                category = category.parent
            if category == self:
                logical_queryset=Product.objects.filter(product=category)
                if logical_queryset.exists():
                    products.append(logical_queryset)
        return set(products)
    @property
    def cout_product(self):

        p=self.get_products_recursively()
        return len(p)
        # return Product.objects.filter(product=self).all().count()











class Product(Status):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    category=models.ForeignKey(Category, on_delete=models.CASCADE,name="product")
    detail_id =  models.ManyToManyField(Detail)
    count = models.PositiveIntegerField()
    price = models.FloatField()
    objects=CustomBaseManager()

    def clean_price(self):
        if not 0<self.price<10000:
            raise ValidationError("Price must be positive and smaller than 10000")
        return True
    

class Comment(Status):
    content=models.TextField(max_length=600)
    is_ok=models.BooleanField(default=False)
    parent=models.ForeignKey("self",on_delete=models.SET("replyed to a deleted comment"),null=True,blank=True)
    item_id=models.ForeignKey(Product,on_delete=models.CASCADE)
    objects=CustomBaseManager()

class DicountPercent(Status):
    expiration=models.DateTimeField()
    percent=models.FloatField(default=0.0)
    product_id=models.ManyToManyField(Product)
    objects=CustomBaseManager()
    
    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(percent__gt=0), name="positive_percent"
            ),
        ]

