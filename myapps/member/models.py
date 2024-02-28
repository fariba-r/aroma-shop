from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import validate_email, RegexValidator
from .manager import CustomUserManager
from ..core.manager import CustomBaseManager,DeleteMixin
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group


class CustomUser(AbstractUser):
    phonenumber = models.CharField(max_length=50, validators=[RegexValidator(
        regex=r'^(?:\+98|0)?9[0-9]{2}(?:[0-9](?:[ -]?[0-9]{3}){2}|[0-9]{8})$',
        message="Invalid phone number format. Example: +989123456789 or 09123456789", ),
    ], verbose_name="Phone number", unique=True)
    email = models.EmailField(max_length=80, verbose_name="email address", validators=[validate_email],
                              unique=True)
    
   
    password = models.CharField(max_length=200)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    
    REQUIRED_FIELDS = ["email","first_name","last_name","phonenumber" ]
    
    def __str__(self):
        return f"{self.first_name}  {self.last_name}"

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    objects = CustomUserManager()
class Status(models.Model):
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='%(class)s')
    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.save()

    def hard_delete(self):
        super().delete()

    def undelete(self):
        self.is_deleted = False
        self.save()

# Create your models here.



class Province(Status,DeleteMixin):
    name=models.CharField(max_length=100,unique=True)
    objects=CustomBaseManager()


def __str__(self):
    return f"{self.name}"


    
    
class City(Status,DeleteMixin):
    province_id=models.ForeignKey(Province,on_delete=models.SET("deleted"),related_name='province')
    name=models.CharField(max_length=100,unique=True)
    objects=CustomBaseManager()

    def __str__(self):
        return f"{self.name} {self.province_id}"








class UserAddress(models.Model):
    user_id=models.ForeignKey(CustomUser, related_name="user",on_delete=models.CASCADE)
    city=models.ForeignKey(City,on_delete=models.PROTECT)
    description=models.TextField(max_length=200)
    is_deleted=models.BooleanField(default=False)

    objects = CustomBaseManager()

    def __str__(self):
        return f"{self.user_id} {self.city}"

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.save()
class Staff(Status):
    POSITOINS=[
        ("controller","controller"),
        ("operator","operator"),
        ("observer","observer"),
    ]

    user_id = models.OneToOneField(CustomUser, related_name="customuser", on_delete=models.CASCADE)
    expiration=models.DateTimeField()
    position=models.CharField(max_length=100,choices=POSITOINS)
    salary=models.PositiveIntegerField()
    objects = CustomBaseManager()



class Admin(CustomUser):
    class Meta:
        proxy=True

    def save(self, *args, **kwargs):
        group = Group.objects.get(name='"Administrators"')
        self.groups.add(group)
        super().save(*args, **kwargs)

