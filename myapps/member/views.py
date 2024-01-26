from django.shortcuts import render,redirect
from django.views.generic import ListView, View, CreateView, TemplateView, FormView, UpdateView
from django.contrib.auth.views import LoginView
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from .forms import CustomUserAuthenticationForm,EmailLoginForm
from django.views.generic import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from .models import CustomUser
from django.http import JsonResponse
# Create your views here.

class LoginPassView(LoginView):
   
    template_name="member/loginpass.html"
    
    def get_success_url(self):
        return reverse_lazy('core:home') 
    
    def form_invalid(self, form):
        messages.error(self.request,'Invalid username or password')
        return self.render_to_response(self.get_context_data(form=form))
    
class LoginEmailView(View):
    def post(self,request,*args,**kwargs):

        code = request.POST['code']
        email = request.POST['email']
        try:
                # check
                return redirect(reverse_lazy('core:home'))
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

   

class ValidateEmailView(View):
    def post(self,request,*args,**kwargs):
        email = request.POST['email']
        try:
            CustomUser.objects.get(email=email)
            return JsonResponse({'valid': 'true'})
        except:
            return  JsonResponse({'valid': 'false'})

