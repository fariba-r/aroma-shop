from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser,Staff
  # Assuming you're using the built-in User model

from django.contrib.auth.models import Group, Permission


@receiver(post_save, sender=Staff)
@receiver(post_save, sender=CustomUser)

def handel_groups(sender, instance, created, **kwargs):
        if instance._meta.verbose_name=="user":
            group = Group.objects.get(name='autenticated')
            instance.groups.add(group)
        else:
            if instance.position == "controller":
                group = Group.objects.get(name='master_product')
            elif instance.position == "operator":
                group = Group.objects.get(name='operator')
            elif instance.position == "observer":
                group = Group.objects.get(name='controller')
                instance.user_id.groups.add(group)

        # instance.save()
