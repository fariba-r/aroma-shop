from django.contrib import admin
from .models import *

admin.site.register(Image)

# //admin.site.register(Like)
admin.site.register(Edites)

# Register your models here.
class LikeAdmin(admin.ModelAdmin):
    pass


admin.site.register(Like, LikeAdmin)

