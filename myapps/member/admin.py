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
    search_fields = ['city', 'user_id', 'is_deleted']

    list_filter = ['user_id']
    list_display = ['user_id', 'city', 'is_deleted']
    editable_list = ['is_deleted']

    def get_queryset(self, request):
        # Include deleted objects
        return UserAddress.objects.archive()


admin.site.register(UserAddress, YourModelAdmin)
