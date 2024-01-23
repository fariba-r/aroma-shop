
from django.contrib.auth.models import BaseUserManager
from ..core.manager import CustomBaseManager,DeleteMixin

class CustomUserManager(DeleteMixin,CustomBaseManager,BaseUserManager):
    def create_user(self, firstname,lastname,phone, email,username, password, **extra_fields):
        """
        Creates and saves a User with the given phonenumber,email and password.
        """
        if not username or not password:
            raise ValueError("Users must have username and password")
        
        user = self.model(first_name=firstname,last_name=lastname,phonenumber=phone,email= email,username=username, password=password, **extra_fields)
        user.set_password(password)
        user.is_active = False
        user.save(using="default")
        return user

    def create_superuser(self,first_name,last_name,phonenumber, email,username, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given phonenumber, nickname, email and password.
        """
        user = self.create_user(
           firstname=first_name,lastname=last_name,phone=phonenumber,email= email,username=username, password=password, **extra_fields
        )
        user.is_admin = True
        user.is_superuser=True
        user.is_active=True
        user.is_staff = True
        user.set_password(password)
        user.save(using="default")
        return user
