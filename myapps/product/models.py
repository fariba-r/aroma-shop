from charset_normalizer import models
from django.contrib import messages
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.shortcuts import redirect
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
    product=models.ForeignKey('Product',on_delete=models.CASCADE,related_name="detaill",name="detaill",null=True,blank=True)
    dependency=models.ForeignKey('self',on_delete=models.CASCADE,null=True,blank=True,related_name="dependencyy")
    objects=CustomBaseManager()

    def __str__(self):
        return f" {self.name}:{self.value}_{self.detaill}"
    @property
    def detail_line(self):
        return Detail.objects.prefetch_related("dependencyy").filter(dependency=self)
    @staticmethod
    def query_list(self,query):
        listt=[]
        for i in query:
            listt.append(i)
        return listt



    
class Category(Status):
    title = models.CharField(max_length=50, unique=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='detail')
    objects = CustomBaseManager()
    def __str__(self):
        return f" {self.title} {self.parent}"

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


        return products
    @property
    def count_product(self):


        p=self.get_products_recursively()
        return len(p)
        # return Product.objects.filter(product=self).all().count()


    def list_to_queryset(self, data):

       return Product.objects.filter(pk__in=data)

    def childrn(self):
        print(Category.objects.filter(parent=self))
        return Category.objects.filter(parent=self)




class Product(Status):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=500)

    category=models.ForeignKey(Category, on_delete=models.CASCADE,name="product",related_name="product")
    comments=GenericRelation('Comment')
    def __str__(self):
        return f" {self.title} "

    objects=CustomBaseManager()
    @property
    def base_group(self):

        return Detail.objects.filter(dependency=None, detaill=self.id)

    def list_base_group_id(self):
        id=[]
        for i in self.base_group:
            id.append(i.id)
        return id

    def all_categoryes(self):
        all_cat=[]
        cat=self.product
        while(cat is not None):
            all_cat.append(cat.id)
            cat=cat.parent
        all_cat=reversed(all_cat)
        return Category.objects.filter(pk__in=all_cat)

    def clean_price(self):
        if not 0<self.price<10000:
            raise ValidationError("Price must be positive and smaller than 10000")
        return True
    






class Comment(Status):
    content=models.TextField(max_length=600)
    is_ok=models.BooleanField(default=False)
    parent=models.ForeignKey("self",on_delete=models.SET("replyed to a deleted comment"),null=True,blank=True)
    item_id=models.ForeignKey(Product,on_delete=models.CASCADE,related_name="comment")
    objects=CustomBaseManager()
    def __str__(self):
        return f" {self.creator} {self.item_id}"
    @property
    def find_replied(self):
        # replied=[]
        for comment in  Comment.objects.filter(item_id=self.item_id ,parent__isnull=False):
            if comment.parent.id==self.id:
                return comment
        # return Comment.filter(id__in=replied)



class DicountPercent(Status):
    expiration=models.DateTimeField()
    percent=models.FloatField(default=0.0)
    detail_id=models.ForeignKey(Detail,on_delete=models.SET("the product delete"))
    objects=CustomBaseManager()
    def __str__(self):
        return f" {self.detail_id} "
    
    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(percent__gt=0), name="positive_percent"
            ),
        ]

class StaffAccessMixin():
    def dispatch(self, request, *args, **kwargs):
        # Check if the user is authenticated (LoginRequiredMixin already handles this)
        if not request.user.groups.filter(name__in=["master_product","controller","operator"]).exists():
            url=request.META.get('HTTP_REFERER')
            messages.warning(request, "You should be staff to reply.")
            return redirect(url)

        return super().dispatch(request, *args, **kwargs)