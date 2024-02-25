# import jwt
# from jwt import exceptions
#
# from django.conf import settings
# from django.contrib.auth import get_user_model
# from django.contrib import messages
# from django.shortcuts import redirect
#
#
# class JWTAuthenticateMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
#
#     def __call__(self, request):
#
#         if token := request.COOKIES.get('jwt'):
#             # print(token)
#             try:
#
#                 # payload = jwt.decode(token, 'secret', algorithms=['HS256'])
#                 payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
#                 user = get_user_model().objects.filter(id=payload.get('id')).first() or \
#                        get_user_model().objects.filter(id=payload.get('user_id')).first()
#                 if user and user.is_active:
#                     request.user = user
#                     # print(request.user)
#             except Exception as e:
#                 # print('error: ', e)
#                 pass
#
#         response = self.get_response(request)
#         response['X-User'] = str(request.user)
#
#         # print(response)
#         # print(dir(response))
#         return response


# ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
from typing import Optional, Tuple

import jwt
from jwt import exceptions
from rest_framework.request import Request
from rest_framework_simplejwt import authentication
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.shortcuts import redirect
from rest_framework_simplejwt.authentication import AuthUser
from rest_framework_simplejwt.tokens import Token
from django.utils.deprecation import MiddlewareMixin

# class JWTAuthentication(authentication.JWTAuthentication):
    # def get_header(self, request: Request) -> bytes:
    #     if token := request.COOKIES.get('jwt'):
    #         print(token)
    #         return token
    #
    #     return ''

    #
    # def authenticate(self, request):
    #     header = self.get_header(request)
    #
    #     if header is None:
    #         raw_token = request.COOKIES.get('jwt') or None
    #     else:
    #         raw_token = self.get_raw_token(header)
    #     print("tokennnnnnnnnnnnnnnnnnnn",raw_token)
    #     if raw_token is None:
    #         return None
    #     raw_token=bytes(raw_token, 'utf-8')
    #     print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",type(raw_token))
    #     validated_token = self.get_validated_token(raw_token)
    #
    #     print(self.get_user(validated_token))
    #     return self.get_user(validated_token), validated_token






# class JWTAuthenticateMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
#
#
#     def __call__(self, request):
#         response = self.get_response(request)
#         if request.user:
#             # response.set_cookie("jwt",)
#             pass
#         return response
#
#     def process_view(self, request, view_func, view_args, view_kwargs):
#         request.user = (_ := JWTAuthentication().authenticate(request)) and _[0]
#         print(request.user)
#         print(request.user)
#
#
class JWTAuthenticateMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if token := request.COOKIES.get('jwt'):
                # print(token)
                try:

                    # payload = jwt.decode(token, 'secret', algorithms=['HS256'])
                    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
                    user = get_user_model().objects.filter(id=payload.get('id')).first() or \
                           get_user_model().objects.filter(id=payload.get('user_id')).first()
                    if user and user.is_active:
                        request.user = user
                        print(request.user)
                    else:
                        print("not user found")
                except Exception as e:
                    print('error: ', e)
                    pass
