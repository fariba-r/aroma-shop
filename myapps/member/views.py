import requests
from django.shortcuts import render,redirect
from django.views.generic import ListView, View, CreateView, TemplateView, FormView, UpdateView
from django.contrib.auth.views import LoginView
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .forms import CustomUserAuthenticationForm,EmailLoginForm
from django.views.generic import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from .models import CustomUser
from rest_framework.views import APIView
from .serializers import GetEmail,Code,Active
from django.core.cache import cache
import pyotp
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from .serializers import LoginSerializer
from rest_framework.permissions import IsAuthenticated

from django.http import JsonResponse
# Create your views here.

# class LoginPassView(LoginView):
#
#
#     template_name="member/loginpass.html"
#
#     def get_success_url(self):
#         return reverse_lazy('core:index')
#
#     def form_invalid(self, form):
#
#         messages.error(self.request,'Invalid username or password')
#         return self.render_to_response(self.get_context_data(form=form))

class LoginPassView(TemplateView):
    template_name = "member/loginpass.html"




class LoginPassAPIView(APIView):
    def post(self,request):
        serializer = LoginSerializer( data=request.data)
        if serializer.is_valid():
            username = serializer['username']
            password = serializer['password']
            user = authenticate(username=username.value, password=password.value)
            if user:

                    login(request, user)

                    return  Response({"message":"login successfully",'status':200})
            else:
                    messages.error(request, 'username or password is not correct !')  # Customize the error message
                    return Response({"status":404,"message":"username or email isn't correct"})
        else:
                messages.error(request, 'somthing went wrong please try again.')
                return Response({"status":500,"message":"somthing went wrong"})

class LoginEmailView(View):
    def post(self,request,*args,**kwargs):

        code = request.POST['code']
        email = request.POST['email']
        try:
                # check
                return redirect(reverse_lazy('core:index'))
        except CustomUser.DoesNotExist:
                messages.error(self.request, 'this email does not exist')
                return render(request, 'member/emaillogin.html')




    def get(self,request,*args,**kwargs):
        # form = EmailLoginForm()
        return render(request, 'member/emaillogin.html', )


        
    
    

class SignUpView(SuccessMessageMixin,CreateView):
    model =CustomUser
    form_class = CustomUserAuthenticationForm
    template_name ="member/signup.html"
    success_url = reverse_lazy('member:loginpass')
    success_message = "Your account was created successfully"

   

# class ValidateEmailView(View):
#     def post(self,request,*args,**kwargs):
#         email = request.POST['email']
#         try:
#             CustomUser.objects.get(email=email)
#             return JsonResponse({'valid': 'true'})
#         except:
#             return  JsonResponse({'valid': 'false'})

class ValidateEmailView(APIView):
    @staticmethod
    def create_code():
        secret_key = 'sseeccrreett'
        totp = pyotp.TOTP(secret_key)
        return totp.now()

    def post(self,request,*args,**kwargs):
        serializer=GetEmail(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors,status=400)
        email=serializer.validated_data['email']

        valid=CustomUser.objects.filter(email=email)

        if len(valid) == 0:
             return Response({'error':'Email does not exist'}, status=400)
        else:
            # send code
            code=self.__class__.create_code()
            cache.set(email, code, timeout=600)
            print("a"*50,code)
            send_mail(
                "Aroma Shop code",
                f" this is your login code:{code}",
                None,  # use default from_email
                [email],  # recipient list
                fail_silently=False,
            )
            # cached_value = cache.get(email)
            return  Response({'succes':'Email  exist'}, status=200)


class ValidateCodeView(APIView):


    def post(self,request,*args,**kwargs):
        serializer=Code(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors,status=400)
        recieved_code=serializer.validated_data['code']
        email = serializer.validated_data['email']

        cashed_code=cache.get(email)

        if recieved_code != cashed_code:
             return Response( status=400)
        else:
            user_obj=CustomUser.objects.get(email=email)
            username = user_obj.username
            password = user_obj.password
            user = authenticate(request, username=username, password=password)
            login(request,user)
            print("loginnnnnnnnnnnnnnnnnnnnnnnnnnnn",request.user)
            return  Response(status=200)


class ActivateAPIView(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self,request):
        code = ValidateEmailView.create_code()

        cache.set(request.user.email, code, timeout=600)
        print("a" * 50, code)
        send_mail(
            "Aroma Shop code",
            f" this is your activate code:{code}",
            None,  # use default from_email
            [request.user.email],  # recipient list
            fail_silently=False,
        )
        return render(request,"member/activate.html")

    def post(self,request):
        serializer = Active(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        recieved_code = serializer.initial_data['code']
        email = request.user.email

        cashed_code = cache.get(email)

        if recieved_code != cashed_code:
            return Response(status=400)
        else:
            request.user.is_active=True;
            return Response(status=200)


