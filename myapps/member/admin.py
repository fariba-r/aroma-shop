from django.contrib import admin
from .models import *

admin.site.register(CustomUser)

admin.site.register(Staff)
admin.site.register(UserAddress)
admin.site.register(Province)
admin.site.register(City)

# Register your models here.
