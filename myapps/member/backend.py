# backends.py
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.core.mail import send_mail

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user_model = get_user_model()
        try:
            user = user_model.objects.get(email=username)
            send_mail(
                        'Hello from Django',
                        'This is a test email.',
                        
                        [user.email],
                        fail_silently=False,
                        )
        except user_model.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None
