from django.db import models
from ..member.models import CustomUser
from django.core.exceptions import ValidationError
from django.db import models
from ..core.manager import CustomBaseManager
from ..member.models import Status
from django.db.models.base import ModelBase


    
class Detail(Status):
    name = models.CharField(max_length=50)
    value = models.CharField(max_length=50)
    product=models.ForeignKey('Product',on_delete=models.CASCADE)
    dependency=models.ForeignKey('self',on_delete=models.CASCADE,null=True,blank=True,name="dependency")
    objects=CustomBaseManager()
    @property
    def detail_line(self):
        return Detail.objects.prefetch_related("dependency").filter(parent=self)


    
class Category(Status):
    title = models.CharField(max_length=50, unique=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='detail')
    objects = CustomBaseManager()

    def get_products_recursively(self):
        products = []
        for category in self.__class__.objects.all():
            old_cat=category
            while (category  is not None):

                if category == self:
                    logical_queryset=Product.objects.filter(product=old_cat)
                    if logical_queryset.exists():
                        for pr in logical_queryset:
                            products.append(pr.id)
                category = category.parent

            logical_queryset = Product.objects.filter(product=category)
            if logical_queryset.exists():
                for pr in logical_queryset:
                    products.append(pr.id)
        return products
    @property
    def cout_product(self):

        p=self.get_products_recursively()
        return len(p)
        # return Product.objects.filter(product=self).all().count()

    def list_to_queryset(self, data):

       return Product.objects.filter(pk__in=data)







class Product(Status):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    category=models.ForeignKey(Category, on_delete=models.CASCADE,name="product")
    objects=CustomBaseManager()
    @property
    def base_group(self):

        return Detail.objects.filter(parent=None, object_id=self.id)


    def clean_price(self):
        if not 0<self.price<10000:
            raise ValidationError("Price must be positive and smaller than 10000")
        return True
    
    def all_categoryes(self):
        all_cat=[]
        cat=self.product
        while(cat is not None):
            all_cat.append(cat.id)
            cat=cat.parent
        all_cat=reversed(all_cat)
        return Category.objects.filter(pk__in=all_cat)





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

