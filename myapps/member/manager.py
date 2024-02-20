from django.db import models
from rest_framework.decorators import api_view, permission_classes


class LogicalQuerySet(models.QuerySet):

    def delete(self):
        return super().update(is_deleted=True)

    def hard_delete(self):
        return super().delete()


class CustomBaseManager(models.Manager):
    def get_queryset(self):
        return LogicalQuerySet(self.model).filter(is_deleted=False)

    def archive(self):
        return LogicalQuerySet(self.model)

    def deleted(self):
        return LogicalQuerySet(self.model).filter(is_deleted=True)


class DeleteMixin():
    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.save()

    def hard_delete(self):
        super().delete()

    def undelete(self):
        self.is_deleted = False
        self.save()





