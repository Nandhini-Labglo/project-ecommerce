from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from requests import request

from website.models import Product, Cart, Order, Wishlistitems
from django.views.generic.list import ListView

from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.db.models import Q
from django.db.models import F, Sum
# Create your views here.

@login_required
def index(request):
    return render(request, 'index.html')

def product_view(request):
        products = Product.objects.all()
        wish_item,created = Wishlistitems.objects.get_or_create(user=request.user)
        wishedProducts = wish_item.product.all()
        w = list(wishedProducts)
        context = {'product': products,'wish':w}
        return render(request, 'product_view.html', context)

class SearchView(ListView):
    model = Product
    template_name = 'search_product.html'
    context_object_name = 'all_search_results'

    def get_queryset(self):
        result = super(SearchView, self).get_queryset()
        query = self.request.GET.get('search')
        print(query)
        if query:
            postresult = Product.objects.filter(
                Q(title__icontains=query) | Q(brand__brand_name__icontains=query), in_stock=True)
            result = postresult
        else:
            result = Product.objects.none()
        return result
    
    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        wish_item = Wishlistitems.objects.get(user=self.request.user.id)
        wishedProducts = wish_item.product.all()
        context['cc'] = wishedProducts
        print(context)
        return context
    

def cart_detail(request):
    if request.user.is_authenticated:
        user = request.user
        carts = Cart.objects.filter(Q(user=user) & Q (is_active=True))
        price = carts.aggregate(total=Sum(F('quantity')*F('price')))
    context = {'form': carts,'price':price}
    return render(request, 'cart.html', context)

@login_required
def add_to_cart(request, product_id):
    if request.method == "POST":
        product = get_object_or_404(Product, id=product_id)
        cart, created = Cart.objects.get_or_create(
            product=product,
            price = product.price,
            quantity = 0,
            user=request.user,
            is_active=True
        )
        cart = Cart.objects.filter(
            product=product,
            price=product.price,
            user=request.user,
            is_active=True
        )[0]
        cart.quantity += 1
        cart.save()
        messages.info(request, "This item quantity was updated.")
    return redirect('view_product')

def remove_item_cart(request, product_id):
    if request.method == "POST":
        product = get_object_or_404(Product, id=product_id)
        cart = Cart.objects.filter(
            product=product,
            user=request.user,
            price=product.price,
            is_active=True
        )[0]
        if cart.quantity > 1:
            cart.quantity -= 1
            cart.save()
        else:
            cart.delete()
            messages.info(request, "This item quantity was updated.")
            return redirect('cart')
    return redirect('cart')
    
def remove_cart(request, cart_id):
    print(request.method)
    if request.method == "POST":
        cart = get_object_or_404(Cart, id=cart_id)
        cart.delete()
    return redirect('cart')

def order_history(request):
    order = Order.objects.filter(user=request.user)
    context = {'order':order}
    return render(request, 'order_history.html',context)

@login_required
def order_placed(request):
    user = request.user
    cart = Cart.objects.filter(Q(user=user) & Q(is_active=True))
    price = cart.aggregate(total=Sum(F('quantity')*F('price')))
    tax_charges = cart.aggregate(tax=Sum(F('quantity')*F('price')*0.18))
    grand_total = cart.aggregate(grand_total=Sum(F('quantity')*F('price')*0.18 + (F('quantity')*F('price'))))
    if cart:
        order = Order.objects.create(user=user, total_product_price=price['total'], total_tax=tax_charges['tax'], total_order_price=grand_total['grand_total'])
        order.product.add(*cart)
        cart.update(is_active=False)
        #orders.update(total_product_price=price['total'],total_tax=tax_charges['tax'],total_order_price=grand_total['grand_total'])
    else:
        orders = Order.objects.latest('id')
    return render(request, 'orders.html',{'orders':orders})

def cancel_order(request, cart_id):
    print(request.method)
    if request.method == "POST":
        cart = get_object_or_404(Cart, id=cart_id)
        cart.delete()
        order =  Order.objects.filter(user=request.user)
    return redirect('order_history')


def add_to_wishlist(request, product_id):
    print(request.method)
    if request.method == "POST":
        products = Product.objects.get(id=product_id)
        wishlist,created = Wishlistitems.objects.get_or_create(user=request.user)
        wishlist.product.add(products)
        messages.success(request, "Added " + products.title + " to your WishList")
    return redirect('view_product')

def remove_from_wishlist(request, product_id):
    print(request.method)
    if request.method == "POST":
        products = get_object_or_404(Product, id=product_id)
        wishlist = get_object_or_404(Wishlistitems, user=request.user)
        wishlist.product.remove(products)
        messages.success(request, products.title + " has been removed from your WishList")
    return redirect('view_product')

@login_required
def view_wishlist(request):
    wishlist = Wishlistitems.objects.filter(user=request.user)
    return render(request, 'wishlist.html', {'wlist': wishlist})
