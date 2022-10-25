from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from decimal import Decimal as D
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

class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=True)
    price = models.FloatField(null=True)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return '{}'.format(self.product)

    
    def get_total(self):
        total = self.product.price * self.quantity
        return total

    def get_final_price(self):
        return self.get_total()

    

class Order_pl(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ManyToManyField(Cart)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return '{}'.format(self.user)
    
    def get_total_items(self):
        total = 0
        for product in self.product.all():
            total = sum(product.quantity)
        return total

    
    def get_total_price(self):
        total = 0
        for order_item in self.product.all():
            total += order_item.get_total()
        return total


        
