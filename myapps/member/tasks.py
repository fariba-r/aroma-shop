from datetime import timezone
from celery import shared_task
from celery.schedules import crontab


from .models import CustomUser

@shared_task
def delete_inactive_users():

     # inactive_users = CustomUser.objects.filter(
     #     created_at__in=timezone.now() - timezone.timedelta(days=3),
     #     is_active=False
     # )
     # # Delete the inactive users
     # inactive_users.delete()

     print("heloooooo")