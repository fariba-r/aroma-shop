from django.db import models

# Create your models here.
from django.db import models
class Status(models.Model):
    is_deleted = models.BooleanField()
    created_at = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey('User', on_delete=models.CASCADE)

    class Meta:
        abstract = True
class Item(Status):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    category_id = models.ForeignKey(Category)
    detail_id =  models.ForeignKey(Detail)
    count = models.IntegerField()
    price = models.FloatField()
    
