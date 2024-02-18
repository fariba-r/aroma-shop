import jwt
from jwt import exceptions

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.shortcuts import redirect


class JWTAuthenticateMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if token := request.COOKIES.get('jwt'):
            try:
                # payload = jwt.decode(token, 'secret', algorithms=['HS256'])
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
                user = get_user_model().objects.filter(id=payload.get('id')).first() or \
                       get_user_model().objects.filter(id=payload.get('user_id')).first()
                if user and user.is_active:
                    request.user = user
            except Exception as e:
                print('error: ', e)
                pass

        response = self.get_response(request)

        return response