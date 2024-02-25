from datetime import datetime, timedelta

import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed, ParseError





class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        # todo:go with token
        if token := request.COOKIES.get('jwt'):
            # print(token)
            try:
                # payload = jwt.decode(token, 'secret', algorithms=['HS256'])
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
                user = get_user_model().objects.filter(id=payload.get('id')).first() or \
                       get_user_model().objects.filter(id=payload.get('user_id')).first()
                if user and user.is_active:
                    return user,payload

            except Exception as e:
                print('error: ', e)
                return None



    def authenticate_header(self, request):
        return 'Bearer'

