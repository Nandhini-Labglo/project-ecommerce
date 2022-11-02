from django.contrib import admin
from website.models import Brand, Product, Cart, Order, Wishlistitems

# Register your models here.

class Brandadmin(admin.ModelAdmin):
    list_display = ['id','brand_name','brand_logo']
admin.site.register(Brand, Brandadmin)

class productadmin(admin.ModelAdmin):
    list_display = ['id','title','image','price','in_stock']
admin.site.register(Product, productadmin)

class cartadmin(admin.ModelAdmin):
    list_display = ['product','user','quantity','is_active','price']
admin.site.register(Cart, cartadmin)

class orderadmin(admin.ModelAdmin):
    list_display = ['user','status','total_product_price','total_tax','total_order_price']
admin.site.register(Order, orderadmin)

class wishadmin(admin.ModelAdmin):
    list_display = ['user']
admin.site.register(Wishlistitems, wishadmin)