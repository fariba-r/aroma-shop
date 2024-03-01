from datetime import timezone
from celery import shared_task
from celery.schedules import crontab


from .models import CustomUser

@shared_task
def delete_inactive_users():
     three_days_ago = timezone.now() - timezone.timedelta(days=3)
     inactive_users = CustomUser.objects.filter(
          created_at__lt=three_days_ago,
          active_status=False
     )

     inactive_users.delete()