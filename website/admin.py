from django.contrib import admin
from website.models import Product, Cart, Order_pl
# Register your models here.

class productadmin(admin.ModelAdmin):
    list_display = ['title','brand','image','price','stock']
admin.site.register(Product, productadmin)

class cartadmin(admin.ModelAdmin):
    list_display = ['product','user','quantity','created_at','is_active']
admin.site.register(Cart, cartadmin)

class orderadmin(admin.ModelAdmin):
    list_display = ['user','order_date','status']
admin.site.register(Order_pl, orderadmin)