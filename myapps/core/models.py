from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from ..product.models import Status
from django.core.files import storage
import os
# Create your models here.
class Like(Status):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    
    content_object = GenericForeignKey('content_type', 'object_id')

class CustomStorage(storage.FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        print("name"*20,name)
        # Get the file extension
        ext = os.path.splitext(name)[1]
        # Check if the file is an image
        if ext in ['.jpg', '.png', '.gif']:
            # Return a path for images
            return f'images/{name}'
        else:
            # Return a path for other files
            return f'files/{name}'
class Image(Status):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    image = models.ImageField(upload_to="images/",storage=CustomStorage())

class Edites(Status):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    field_changed=models.CharField(max_length=100)
    old_value=models.CharField(max_length=100)