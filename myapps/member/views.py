from django.shortcuts import render
from django.views.generic import ListView, View, CreateView, TemplateView, FormView, UpdateView
from django.contrib.auth.views import LoginView
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from .forms import CustomUserAuthenticationForm
from django.views.generic import CreateView
from django.contrib.messages.views import SuccessMessageMixin
# Create your views here.

class LoginPassView(LoginView):
   
    template_name="member/login.html"
    
    def get_success_url(self):
        return reverse_lazy('core:home') 
    
    def form_invalid(self, form):
        messages.error(self.request,'Invalid username or password')
        return self.render_to_response(self.get_context_data(form=form))
    

class SignUpView(SuccessMessageMixin,CreateView):
    form_class = CustomUserAuthenticationForm
    template_name ="member/signup.html"
    success_url = reverse_lazy('member:login')
    success_message = "Your account was created successfully"

class LoginEmailView():
    pass
