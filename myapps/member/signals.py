from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser,Staff
  # Assuming you're using the built-in User model
from django.core.mail import send_mail
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

@receiver(post_save, sender=CustomUser)
def welcome_email(sender, instance, created, **kwargs):
    if created:
        send_mail(
            "Aroma Shop code",
            f"hello {instance.first_name} {instance.last_name} \n welcome to our shop!\nif you want to shop fro us active your account first.if you don't do that ,your account deleted!\n for activate your account click on this link \n http://127.0.0.1:8000/member/activate_acount/ \n or go to your panel in our site and click on activate ",
            None,  # use default from_email
            [instance.email],  # recipient list
            fail_silently=False,
        )