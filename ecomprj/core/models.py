from django.db import models
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField
from django.contrib.auth import models as auth_models


# Create your models here.



class UserManager(auth_models.BaseUserManager):
    def create_user(self,first_name:str,last_name:str,email:str,password:str=None,is_superuser=False,is_staff=False) -> "User":
        if not email:
            raise ValueError("Укажите почтовый адрес")
        if not first_name:
            raise ValueError("Укажите Ваше имя")
        if not last_name:
            raise ValueError("Укажите Вашу фамилию")
        user = self.model(email=self.normalize_email(email))
        user.first_name = first_name
        user.last_name = last_name
        user.set_password(password)
        user.is_active = True
        user.is_staff = is_staff
        user.is_superuser = is_superuser
        user.save()
        return user

    def create_superuser(self,first_name:str,last_name:str,email:str,password:str) -> "User":
        user = self.create_user(
            first_name = first_name,
            last_name = last_name,
            email = email,
            password = password,
            is_staff = True,
            is_superuser = True
        )
        user.save()
        return user



class User(auth_models.AbstractUser):
    first_name = models.CharField(verbose_name='First Name',max_length=255)
    last_name = models.CharField(verbose_name='Last name',max_length=255)
    email = models.EmailField(unique=True,max_length=255,verbose_name='Email')
    password = models.CharField(max_length=255)
    username = None

    objects = UserManager()


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name","last_name"]




class Product(models.Model):
    CATEGORY_CHOICES = ( 

    ('ONX', 'OnyxBoox'),
    ('PB','PocketBooks'),
    )

    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=7,decimal_places=2)
    description = models.TextField()
    category = models.CharField(choices=CATEGORY_CHOICES,max_length=20)
    composition = models.TextField(default='')
    product_image = models.ImageField(upload_to='product')

    def __str__(self):
        return "{}{}{}{}{}{}".format(self.title, self.price, self.description, self.category, self.composition, self.product_image)

class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    
    @property
    def total_coast(self):
        return self.quantity * self.product.price

    def __str__(self):
        return "{}{}{}".format(self.product,self.quantity,self.total_coast)



STATUS_CHOICES = (('Принят','Принят'),('Упакован','Упакован'),('В пути','В пути'),('Доставлен','Доставлен'),('В ожидании','В ожидании'),)




class Comment(models.Model):
    product = models.ForeignKey(Product,related_name='comments', on_delete=models.CASCADE)
    name = models.CharField(max_length=80)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return "{}{}{}{}{}{}".format(self.body, self.name, self.user, self.updated, self.created, self.product)





    
    