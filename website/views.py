from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from website.models import Product, Cart, Order_pl, Wish_items
from django.views.generic.list import ListView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.db.models import F, Sum
# Create your views here.

@login_required
def index(request):
    return render(request, 'index.html')

@login_required(redirect_field_name='login',login_url='login')
def view(request):
    products = Product.objects.all()
    print(products)
    wish = Wish_items.objects.get(user=request.user)
    print(wish)
    wishedProducts = wish.product.all()
    w = list(wishedProducts)
    print(w)

    context = {'product': products,'wish':w}
    return render(request, 'view.html', context)

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
        carts = Cart.objects.filter(Q(user=user) & Q (is_active=True))
        price = carts.aggregate(total=Sum(F('quantity')*F('price')))
    context = {'form': carts,'price':price}
    return render(request, 'cart.html', context)


def add_to_cart(request, id):
    product = get_object_or_404(Product, id=id)
    cart, created = Cart.objects.get_or_create(
        product=product,
        price = product.price,
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
    return redirect('view_p')

def remove_item_cart(request, id):
    product = get_object_or_404(Product, id=id)
    order_qs = Order_pl.objects.filter(
        user=request.user,
        status='completed'
    )
    if order_qs.exists():
        order = order_qs[0]
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
            order.product.remove(cart)
        messages.info(request, "This item quantity was updated.")
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
        cart = Cart.objects.filter(
            product=product,
            user=request.user,
            price=product.price,
            is_active=True
            )[0]
        order.product.remove(cart)
        cart.delete()
        messages.info(request, "This item was removed from your cart.")
        return redirect('cart')
    else:
        messages.info(request, "You do not have an active order")
        return redirect('cart')

def orderplaced(request):
    user = request.user
    print(user)
    cart = Cart.objects.filter(Q(user=user) & Q(is_active=True))
    price = cart.aggregate(total=Sum(F('quantity')*F('price')))
    tax_charges = cart.aggregate(tax=Sum(F('quantity')*F('price')*0.18))
    grand_total = cart.aggregate(grand_total=Sum(F('quantity')*F('price')*0.18 + (F('quantity')*F('price'))))
    #tax = int(18/100 * price)
    #grand_total = price + tax
    print(cart)
    order = Order_pl.objects.create(user=request.user)
    order.product.add(*cart)
    cart.update(is_active=False)
    orders = Order_pl.objects.filter(user=user, status='completed')
    return render(request, 'orders.html', {'orders': orders,'price':price,'tax_charges':tax_charges,'grand_total':grand_total})

def cancel_order(request,id):
    product = get_object_or_404(Product, id=id)
    order = get_object_or_404(Order_pl, id=id)
    order.product.remove(product)
    return redirect('orderplaced')

def add_to_wishlist(request, id):

   products = Product.objects.get(id=id)
   created,wishlist = Wish_items.objects.get_or_create(user=request.user)
   wishlists = Wish_items.objects.get(user = request.user)
   wishlists.product.add(products)
   messages.success(request, "Added " + products.title + " to your WishList")
   return redirect('view_p')

def remove_from_wishlist(request, id):

   products = get_object_or_404(Product, id=id)
   wishlist = get_object_or_404(Wish_items, user=request.user)
   wishlist.product.remove(products)
   messages.success(request, products.title + " has been removed from your WishList")
   return redirect('view_p')

def view_wishlist(request):
    wishlist = Wish_items.objects.filter(user=request.user)
    #wish = wishlist.product.all()
    return render(request, 'wishlist.html', {'wlist': wishlist})
