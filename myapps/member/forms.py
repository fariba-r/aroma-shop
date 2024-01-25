from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser

class CustomUserAuthenticationForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'firstname',
        'name': 'first_name',
        'placeholder': 'First Name',
        'onfocus': "this.placeholder = ''",
        'onblur': "this.placeholder = 'First Name'"
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'lasttname',
        'name': 'last_name',
        'placeholder': 'Last Name',
        'onfocus': "this.placeholder = ''",
        'onblur': "this.placeholder = 'Last Name'"
    }))
    phonenumber = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'phonenumber',
        'name': 'phonenumber',
        'placeholder': 'Phone Number',
        'onfocus': "this.placeholder = ''",
        'onblur': "this.placeholder = 'Phone Number'"
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'id': 'email',
        'name': 'email',
        'placeholder': 'Email',
        'onfocus': "this.placeholder = ''",
        'onblur': "this.placeholder = 'Email'"
    }))
    
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'username',
        'name': 'username',
        'placeholder': 'Username',
        'onfocus': "this.placeholder = ''",
        'onblur': "this.placeholder = 'Username'"
    }))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'id': 'password',
        'name': 'password',
        'placeholder': 'Password',
        'onfocus': "this.placeholder = ''",
        'onblur': "this.placeholder = 'Password'"
    }))

   
    
    class Meta:
        model = CustomUser
        fields = [ 'first_name', 'last_name', 'phonenumber','email', 'username', 'password']


class EmailLoginForm(forms.Form):
    email = forms.CharField()
    code = forms.CharField()

    widgets = {
        'email':forms.EmailInput(attrs={
        'class': 'form-control',
        'id': 'email',
        'name': 'email',
        'placeholder': 'Email',
        'onfocus': "this.placeholder = ''",
        'onblur': "this.placeholder = 'Email'"
    }),
    'code':forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'code',
        'name': 'code',
        'placeholder': 'Enter Code',
        'onfocus': "this.placeholder = ''",
        'onblur': "this.placeholder = 'Code'"
    })
    }

    def clean_code(self):
        cleaned_data = super().clean()
        code=cleaned_data['code']
        if not (code.isnumeric() and len(code)==5):
            raise ValueError('Invalid code')

