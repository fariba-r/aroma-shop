from django.db import models
class LogicalQuerySet(models.QuerySet):

    def delete(self):
        return super().update(is_deleted=True)

class CustomBaseManager(models.Manager):
    def get_queryset(self):
        return LogicalQuerySet(self.model).filter(is_deleted=False)
    

class DeleteMixin():
    def delete(self, using=None, keep_parents=False):
        print("vvvvvvvvvvvvvv"*10)
        self.is_deleted = True
        self.save()

    



