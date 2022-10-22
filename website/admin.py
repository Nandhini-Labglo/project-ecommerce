from django.contrib import admin
from website.models import Product, cart
# Register your models here.

class productadmin(admin.ModelAdmin):
    list_display = ['title','brand','image','price','stock']
admin.site.register(Product, productadmin)

class cartadmin(admin.ModelAdmin):
    list_display = ['product','user','quantity','created_at','price']
admin.site.register(cart, cartadmin)