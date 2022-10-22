from email.policy import default
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Product(models.Model):
    title = models.CharField(max_length=30)
    brand = models.CharField(max_length=30)
    image = models.ImageField(upload_to='images/products')
    price = models.FloatField(default=100.0)
    description = models.CharField(max_length=30, blank=True)
    stock = models.BooleanField(default=True)

    def __str__(self):
        return '{} {}'.format(self.title,self.brand)

class cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=True,null=True)
    price = models.FloatField(default=100.0)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return '{}'.format(self.product)


        
