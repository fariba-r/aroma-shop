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
from .serializers import GetEmail
from django.http import JsonResponse
# Create your views here.

class LoginPassView(LoginView):
   
    template_name="member/loginpass.html"
    
    def get_success_url(self):
        return reverse_lazy('core:index')
    
    def form_invalid(self, form):
        messages.error(self.request,'Invalid username or password')
        return self.render_to_response(self.get_context_data(form=form))
    
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
    def post(self,request,*args,**kwargs):
        serializer=GetEmail(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors,status=400)
        email=serializer.validated_data['email']

        valid=CustomUser.objects.filter(email=email)

        if len(valid) == 0:
             return Response({'error':'Email does not exist'}, status=400)

        return  Response({'succes':'Email  exist'}, status=200)



