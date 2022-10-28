from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from website.models import Product, Cart, Order_pl, Wishli
from django.views.generic.list import ListView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
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
                messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


@login_required(redirect_field_name='login', login_url='login')
def logout_request(request):
	logout(request)
	return redirect('login')


@login_required(redirect_field_name='next', login_url='login')
def index(request):
    return render(request, 'index.html')


def view(request):
    products = Product.objects.all()
    print(products)
    #user=request.user
    wish = Wishli.objects.get(user=request.user)
    print(wish)
    wishedProducts = wish.product.all()
    w = list(wishedProducts)
    print(w)

    context = {'product': products,'wish':w}
    return render(request, 'view.html', context)


class ProductListview(ListView):
    model = Product
    fields = '__all__'
    template_name = 'product_view.html'
    context_object_name = 'all_search_results'


class SearchView(ListView):
    model = Product
    template_name = 'product.html'
    context_object_name = 'all_search_results'

    def get_queryset(self):
        result = super(SearchView, self).get_queryset()
        query = self.request.GET.get('search')
        if query:
            postresult = Product.objects.filter(
                Q(title__icontains=query) | Q(brand__icontains=query), stock=True)
            result = postresult
        else:
            result = None
        return result


def cart_detail(request):
    if request.user.is_authenticated:
        user = request.user
        carts = Cart.objects.filter(user=user, is_active=True)
        amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        print(cart_product)
        if cart_product:
            for p in cart_product:
                total_price = (p.quantity * p.product.price)
                amount += total_price
    context = {'form': carts, 'amount': amount, }
    return render(request, 'cart.html', context)


def add_to_cart(request, id):
    product = get_object_or_404(Product, id=id)
    cart, created = Cart.objects.get_or_create(
        product=product,
        user=request.user,
        is_active=True
    )
    order_qs = Order_pl.objects.filter(user=request.user, status=True)
    if order_qs.exists():
        order = order_qs[0]
        if order.product.filter(product__id=product.id).exists():
            cart.quantity += 1
            cart.save()
            messages.info(request, "This item quantity was updated.")
            return redirect('view_p')
        else:
            order.product.add(cart)
            messages.info(request, "This item was added to your cart.")
            return redirect('view_p')
    else:
        order_date = datetime.now()
        order = Order_pl.objects.create(
            user=request.user, order_date=order_date)
        order.product.add(cart)
        messages.info(request, "This item was added to your cart.")
        return redirect('view_p')


def remove_item_cart(request, id):
    product = get_object_or_404(Product, id=id)
    order_qs = Order_pl.objects.filter(
        user=request.user,
        status='completed'
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order/cart
        if order.product.filter(product__id=product.id).exists():
            cart = Cart.objects.filter(
                product=product,
                user=request.user,
                is_active=True
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


def remove_cart(request, id):
    product = get_object_or_404(Product, id=id)
    order_qs = Order_pl.objects.filter(
        user=request.user,
        status='completed'
    )
    if order_qs.exists():
        order = order_qs[0]
        if order.product.filter(product__id=product.id).exists():
            cart = Cart.objects.filter(
                product=product,
                user=request.user,
                is_active=True
            )[0]
            order.product.remove(cart)
            cart.delete()
            messages.info(request, "This item was removed from your cart.")
            return redirect('cart')
        else:  # change
            messages.info(request, "This item was not in your cart")
            return redirect('cart')
    else:
        messages.info(request, "You do not have an active order")
        return redirect('cart')


def order(request):
    user = request.user
    orders = Order_pl.objects.filter(user=user, status='completed')
    print(orders)
    messages.info(request, "Your Order is Placed")
    return render(request, 'orders.html', {'orders': orders})


def orderplaced(request):
    user = request.user
    cart = Cart.objects.filter(user=user, is_active=False)
    print(cart)
    for c in cart:
        Order_pl(user=user).save()
        c.delete()
    return redirect('order')


def add_to_wishlist(request, id):

   product = get_object_or_404(Product, id=id)

   product, created = Wishli.objects.get_or_create(product=product,
   id=product.id,
   user=request.user,
   )
   return redirect('view_p')


def view_wishlist(request):
	wlist=Wishli.objects.filter(user=request.user)
	return render(request, 'wishlist.html', {'wlist': wlist})
