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

"""
FAILED = 0
SUCCESS = 1
PENDING = 2


ORDER_STATUS_CHOICES = (
    (SUCCESS, 'Success'),
    (PENDING, 'Pending'),
    (FAILED. 'FAILED'
)  
status = models.Integerield(max_length=1, default=PENDING, choices=ORDER_STATUS_CHOICES)
"""

class TimeStampBaseModel(models.Model):
    created_on =  models.DateTimeField(auto_now_add=True)
    updated_on =  models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True    


class Product(TimeStampBaseModel):
    title = models.CharField(max_length=30)
    brand = models.CharField(max_length=30) # Keep separate model for brand
    image = models.ImageField(upload_to='images/products')
    price = models.FloatField(default=100.0) # how can we have a default price for a product in our DB?
    description = models.CharField(max_length=30, blank=True) # use textfield 
    stock = models.BooleanField(default=True) # in_stock naming

    def __str__(self):
        return '{} {}'.format(self.title,self.brand)

class Cart(TimeStampBaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0) # no product should add to cart without qty
    price = models.FloatField(default=1000.0) # no dft
    is_active = models.BooleanField(default=True) #

    def __str__(self):
        return '{}'.format(self.product)

    
    def get_total(self):
        total = self.price * self.quantity
        return total

    def get_tax(self):
        grand_total = (18/100) * (self.get_total())
        return grand_total



class Order_pl(TimeStampBaseModel): # model shouldn't have any underscore Order
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ManyToManyField(Cart)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=120, default='completed', choices=ORDER_STATUS_CHOICES) 
    """
    Please add the following fields
    total_product_price
    total_tax
    shipping_cost = 
    total_order_value == > Tax+total product price+shipping_cost 
    
    """
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

class Wish_items(TimeStampBaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ManyToManyField(Product)

    def __str__(self):
        return '{}'.format(self.product)
    

    


        
