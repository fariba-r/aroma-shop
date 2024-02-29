from django.contrib import admin
from .models import *



class CustomUserAdmin(admin.ModelAdmin):
    search_fields = ['phonenumber', 'first_name', 'last_name', 'is_deleted',"email"]

    list_filter = ['is_deleted']
    list_display = ['first_name', 'last_name',"email"]
    editable_list = ['is_deleted']

    def get_queryset(self, request):
        # Include deleted objects
        return CustomUser.objects.archive()


admin.site.register(CustomUser, CustomUserAdmin)

class StaffAdmin(admin.ModelAdmin):
    search_fields = ['position', 'user_id__first_name', 'user_id__last_name', 'is_deleted',"salary"]

    list_filter = ['position']
    list_display = [ 'user_id', 'position',"salary", 'is_deleted']
    editable_list = ['is_deleted']

    def get_queryset(self, request):
        # Include deleted objects
        return Staff.objects.archive()


admin.site.register(Staff, StaffAdmin)


class ProvinceAdmin(admin.ModelAdmin):
    search_fields = ['name', 'is_deleted']

    list_filter = ['name']
    list_display = ['name', 'is_deleted']
    editable_list = ['is_deleted']

    def get_queryset(self, request):
        # Include deleted objects
        return Province.objects.archive()


admin.site.register(Province, ProvinceAdmin)


class CityAdmin(admin.ModelAdmin):
    search_fields = ['province_id__name', 'name', 'is_deleted']

    list_filter = ['province_id__name']
    list_display = ['name', 'province_id', 'is_deleted']
    editable_list = ['is_deleted']

    def get_queryset(self, request):
        # Include deleted objects
        return City.objects.archive()


admin.site.register(City, CityAdmin)






class UserAddressAdmin(admin.ModelAdmin):
    search_fields = ['city__name', 'user_id__first_name', 'user_id__last_name', 'is_deleted']

    list_filter = ['user_id']
    list_display = ['user_id', 'city', 'is_deleted']
    editable_list = ['is_deleted']

    def get_queryset(self, request):
        # Include deleted objects
        return UserAddress.objects.archive()


admin.site.register(UserAddress, UserAddressAdmin)
