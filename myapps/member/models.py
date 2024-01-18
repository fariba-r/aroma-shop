from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import validate_email, RegexValidator


# Create your models here.


class Status(models.Model):
    is_deleted=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta:
        abstract=True

class Province(models.Model):
    name=models.CharField(max_length=100,unique=True)
    
    
class City(models.Model):
    province_id=models.ForeignKey(Province,on_delete=models.SET("deleted"),related_name='province')
    name=models.CharField(max_length=100,unique=True)


class CustomUserManager(BaseUserManager):
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

class CustomUser(AbstractUser,Status):
    phonenumber = models.CharField(max_length=50, validators=[RegexValidator(
        regex=r'^(?:\+98|0)?9[0-9]{2}(?:[0-9](?:[ -]?[0-9]{3}){2}|[0-9]{8})$',
        message="Invalid phone number format. Example: +989123456789 or 09123456789", ),
    ], verbose_name="Phone number", unique=True)
    email = models.EmailField(max_length=80, verbose_name="email address", validators=[validate_email],
                              unique=True
                              )
    
   
    password = models.CharField(max_length=200)
    
    REQUIRED_FIELDS = ["email","first_name","last_name","phonenumber" ]
    
    

    objects = CustomUserManager()




class UserAddress(models.Model):
    user_id=models.ForeignKey(CustomUser, related_name="user",on_delete=models.CASCADE)
    city=models.ForeignKey(Province,on_delete=models.PROTECT)
    description=models.TextField(max_length=200)
    is_deleted=models.BooleanField(default=False)

class Staff(Status):
    POSITOINS=[
        ("controller","controller"),
        ("operator","operator"),
        ("observer","observer"),
    ]
    user_id=models.ForeignKey(CustomUser, related_name="customuser", on_delete=models.CASCADE)
    expiration=models.DateTimeField()
    position=models.CharField(max_length=100,choices=POSITOINS)
    salary=models.PositiveIntegerField()

class Admin(CustomUser):
    class Meta:
        proxy=True