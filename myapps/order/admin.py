from django.contrib import admin
from .models import *

admin.site.register(Order)

admin.site.register(DiscountCodeUsed)
admin.site.register(ProductOrder)

# Register your models here.
