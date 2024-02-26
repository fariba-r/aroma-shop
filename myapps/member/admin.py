from django.contrib import admin
from .models import *

admin.site.register(CustomUser)

admin.site.register(Staff)
# admin.site.register(UserAddress)
admin.site.register(Province)
admin.site.register(City)

# Register your models here.
from django.contrib import admin


class YourModelAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        # Include deleted objects
        return UserAddress.objects.archive()

admin.site.register(UserAddress, YourModelAdmin)