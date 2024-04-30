from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.core.validators import EmailValidator

class UserManager(BaseUserManager):

    def create_user(self,email,full_name,age,city ,password = None,**kwargs):

        if not email :
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email,full_name=full_name,age=age,city=city,**kwargs)
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_superuser(self, email, full_name, age, city, password=None, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        return self.create_user(email, full_name, age, city, password, **extra_fields)
    




class User(AbstractBaseUser):
    email = models.EmailField(max_length = 240,validators=[EmailValidator()],unique = True )
    full_name = models.CharField(max_length = 255)
    age = models.IntegerField()
    city = models.CharField(max_length = 100)
    is_admin = models.BooleanField(default = False)
    created_at = models.DateTimeField(auto_now_add = True)
    username = None
    is_staff = None

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name",'age','city']

class FoodProduct(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    average_rating = models.FloatField()
    category = models.CharField(max_length=50)
    product_type = models.CharField(max_length=10, choices=[('Veg', 'Vegetarian'), ('NonVeg', 'Non-Vegetarian')])
    fvrt_by = models.ManyToManyField('User',blank=True)
    
    def __str__(self):
        return f'{self.name} : {self.price}'

class Customization(models.Model):
    name = models.CharField(max_length=255)
    group = models.CharField(max_length=50)
    toppings = models.TextField()
    food_product = models.ForeignKey(FoodProduct, on_delete=models.CASCADE, related_name='customizations')