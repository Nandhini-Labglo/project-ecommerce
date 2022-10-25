from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from website.models import Product, Cart, Order_pl
from website.forms import productForm
from django.views.generic.list import ListView
from django.views import View
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime

# Create your views here.

def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect('index')
            else:
                messages.error(request,"Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

@login_required(redirect_field_name='login',login_url='login')
def logout_request(request):
	logout(request)
	return redirect('login')

@login_required(redirect_field_name='next',login_url='login')   
def index(request):
    return render(request, 'index.html')

def view(request):
    products = Product.objects.all()
    context = {'form':products}
    return render(request,'view.html',context)

class ProductListview(ListView):
    model = Product
    fields = '__all__'
    template_name = 'view.html'
    context_object_name = 'all_search_results'

class SearchView(ListView):
    model = Product
    template_name = 'search.html'
    context_object_name = 'all_search_results'

    def get_queryset(self):
        result = super(SearchView, self).get_queryset()
        query = self.request.GET.get('search')
        if query:
            postresult = Product.objects.filter(Q(title__icontains=query) | Q(brand__icontains=query), stock=True)
            result = postresult
        else:
            result = None
        return result

def cart_detail(request):
    if request.user.is_authenticated:
        user = request.user
        carts = Cart.objects.filter(user=user, is_active=False)
        amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        print(cart_product)
        if cart_product:
            for p in cart_product:
                total_price = (p.product.price)
                amount += total_price
        context = {'form':carts,'amount':amount,}
        return render(request,'cart.html',context)

def add_to_cart(request,id):
    product = get_object_or_404(Product, id=id)
    cart, created = Cart.objects.get_or_create(
        product=product,
        user=request.user,
        is_active=False
    )
    order_qs = Order_pl.objects.filter(user=request.user, status=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.product.filter(product__id=product.id).exists():
            cart.quantity += 1
            cart.save()
            messages.info(request, "This item quantity was updated.")
            return redirect('cart')
        else:
            order.product.add(cart)
            messages.info(request, "This item was added to your cart.")
            return redirect('cart')
    else:
        order_date = datetime.now()
        order = Order_pl.objects.create(user=request.user, order_date=order_date)
        order.product.add(cart)
        messages.info(request, "This item was added to your cart.")
        return redirect('cart')

def remove_item_cart(request, id):
    product = get_object_or_404(Product, id=id)
    order_qs = Order_pl.objects.filter(
        user=request.user,
        status=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order/cart
        if order.product.filter(product__id=product.id).exists():
            cart = Cart.objects.filter(
                product=product,
                user=request.user,
                is_active=False
            )[0]
            if cart.quantity > 1:
                cart.quantity -= 1
                cart.save()
            else:
                order.product.remove(cart)
            messages.info(request, "This item quantity was updated.")
            return redirect('cart')
        else:
            messages.info(request, "This item was not in your cart")
            return redirect('cart')
    else:
        messages.info(request, "You do not have an active order")
        return redirect('cart')


def remove_cart(request):
    if request.method == 'POST':
        prod_id = int(request.POST.get('product_id'))
        if(Cart.objects.filter(product_id=prod_id,user=request.user)):
            c = Cart.objects.get(product_id=prod_id,user=request.user)
            c.delete()
            context = {'status':'updated'}
        return JsonResponse(context)
    return redirect('cart')


def order(request):
    user = request.user
    orders = Order_pl.objects.filter(user=user, status=False)
    print(orders)
    return render(request, 'orders.html', {'orders': orders})


def orderplaced(request):
    user = request.user
    cart = Cart.objects.filter(user=user,is_active=True)
    for c in cart:
       product = c.product
       Order_pl(user=user).save()
       c.delete()
    return redirect('order')