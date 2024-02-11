from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from ..member.models import Status
from .manager import CustomBaseManager

import os


# Create your models here.
class Like(Status):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    objects=CustomBaseManager()

    def __str__(self):
        return f"{self.object_id}"
def get_image_path(instance, filename):
    if instance.content_type_id==7:
        return os.path.join('images','profile', filename)
    if instance.content_type_id==19:
        return os.path.join('images','product', filename)
    if instance.content_type_id==22:
        return os.path.join('images','category', filename)
    else:
        return os.path.join('images', 'other', filename)


class Image(Status):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    image = models.ImageField(upload_to=get_image_path)
    objects=CustomBaseManager()

    def __str__(self):
        return f"{self.object_id} {self.content_type}"

class Edites(Status):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    field_changed=models.CharField(max_length=100)
    old_value=models.CharField(max_length=100)
    objects=CustomBaseManager()

    def __str__(self):
        return f"{self.object_id}"