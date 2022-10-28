from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from decimal import Decimal as D
# Create your models here.

ORDER_STATUS_CHOICES = (
    ('completed', 'Completed'),
    ('pending', 'Pending'),
)

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
    quantity = models.PositiveIntegerField(default=1)
    price = models.FloatField(null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return '{}'.format(self.product)

    
    def get_total(self):
        total = self.product.price * self.quantity
        return total

    def get_final_price(self):
        return self.get_total()

    def get_tax(self):
        grand_total = (18/100) * (self.get_total())
        return grand_total



class Order_pl(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ManyToManyField(Cart)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=120, default='completed', choices=ORDER_STATUS_CHOICES)
    def __str__(self):
        return '{}'.format(self.user)

    def get_total_price(self):
        total = 0
        for order_item in self.product.all():
            total += order_item.get_total()
        return total

    def get_tax(self):
        tax_total = (18/100) * (self.get_total_price())
        return tax_total
    
    def get_grand_total(self):
        grand_total = self.get_total_price() + self.get_tax()
        return grand_total

class Wishli(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ManyToManyField(Product)

    def __str__(self):
        return '{}'.format(self.product)
    

    


        
