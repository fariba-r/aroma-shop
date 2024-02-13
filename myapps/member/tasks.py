from datetime import timezone
from celery.schedules import crontab


from .models import CustomUser

def delete_inactive_users():

     inactive_users = CustomUser.objects.filter(
         created_at__in=timezone.now() - timezone.timedelta(days=3),
         is_active=False
     )
     # Delete the inactive users
     inactive_users.delete()