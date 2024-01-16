from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import validate_email, RegexValidator


# Create your models here.


class Status(models.Model):
    is_deleted=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta:
        abstrac=True

class Province(models.Model):
    name=models.CharField(max_length=100,unique=True)
    
    
class City(models.Model):
    province_id=models.ForeignKey(Province,on_delete=models.SET("deleted"),related_name='province')
    name=models.CharField(max_length=100,unique=True)

class CustomUserManager(BaseUserManager):
    def create_user(self, firstname,lastname,phone, email,created_at,is_deleted,username, password, **extra_fields):
        """
        Creates and saves a User with the given phonenumber,email and password.
        """
        if not username or not password:
            raise ValueError("Users must have username and password")
        
        user = self.model(first_name=firstname,last_name=lastname,phonenumber=phone,email= email,created_at=created_at,is_deleted=is_deleted,username=username, password=password, **extra_fields)
        user.set_password(password)
        user.is_active = False
        user.save(using="postgresql")
        return user

    def create_superuser(self,firstname,lastname,phone, email,created_at,is_deleted,username, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given phonenumber, nickname, email and password.
        """
        user = self.create_user(
           first_name=firstname,last_name=lastname,phonenumber=phone,email= email,created_at=created_at,is_deleted=is_deleted,username=username, password=password, **extra_fields
        )
        user.is_admin = True
       
        user.set_password(password)
        user.save(using="postgresql")
        return user

class CustomerUser(AbstractUser,Status):
    phonenumber = models.CharField(max_length=50, validators=[RegexValidator(
        regex=r'^(?:\+98|0)?9[0-9]{2}(?:[0-9](?:[ -]?[0-9]{3}){2}|[0-9]{8})$',
        message="Invalid phone number format. Example: +989123456789 or 09123456789", ),
    ], verbose_name="Phone number", unique=True)
    email = models.EmailField(max_length=100, verbose_name="email address", validators=[validate_email],
                              unique=True
                              )
    
   
    password = models.CharField(max_length=20)
    
    
    
    

    objects = CustomUserManager()




class UserAddress(models.Model):
    user_id=models.ForeignKey(CustomerUser, related_name="user",ondelete=models.CASCADE)
    city=models.ForeignKey(Province,on_delete=models.PROTECT)
    description=models.TextField(max_length=200)
