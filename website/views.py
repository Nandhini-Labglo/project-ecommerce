from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.shortcuts import render, reverse, redirect, get_object_or_404

from django.contrib.auth.models import User
from website.models import Product, Cart, Order, Wishlistitems, Payment
from django.views.generic.list import ListView
from django.views.generic import View

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.conf import settings

from django.db.models import Q
from django.db.models import F, Sum

import json
import stripe

# Create your views here.


@login_required
def index(request):
    return render(request, 'index.html')


def product_view(request):
    products = Product.objects.all()
    wish_item, created = Wishlistitems.objects.get_or_create(user=request.user)
    wishedProducts = wish_item.product.all()
    w = list(wishedProducts)
    context = {'product': products, 'wish': w}
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


stripe.api_key = settings.STRIPE_SECRET_KEY


def cart_detail(request):
    user = request.user
    carts = Cart.objects.filter(Q(user=user) & Q(is_active=True))
    price = carts.aggregate(total=Sum(F('quantity')*F('price')))
    tax_charges = carts.aggregate(tax=Sum(F('quantity')*F('price')*0.18))
    grand_total = carts.aggregate(grand_total=Sum(
        F('quantity')*F('price')*0.18 + (F('quantity')*F('price'))))
    key = settings.STRIPE_PUBLISHABLE_KEY
    context = {'form': carts, 'price': price,
               'tax_charges': tax_charges, 'grand_total': grand_total, 'key': key}
    return render(request, 'cart.html', context)


@login_required
def add_to_cart(request, product_id):
    if request.method == "POST":
        product = get_object_or_404(Product, id=product_id)
        cart, created = Cart.objects.get_or_create(
            product=product,
            price=product.price,
            quantity=0,
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
    context = {'order': order}
    return render(request, 'order_history.html', context)


@login_required
def order_placed(request):
    user = request.user
    cart = Cart.objects.filter(Q(user=user) & Q(is_active=True))
    price = cart.aggregate(total=Sum(F('quantity')*F('price')))
    tax_charges = cart.aggregate(tax=Sum(F('quantity')*F('price')*0.18))
    grand_total = cart.aggregate(grand_total=Sum(
        F('quantity')*F('price')*0.18 + (F('quantity')*F('price'))))

    if cart:
        orders = Order.objects.create(
            user=user, total_product_price=price['total'], total_tax=tax_charges['tax'], total_order_price=grand_total['grand_total'])
        orders.product.add(*cart)
        cart.update(is_active=False)
    else:
        orders = Order.objects.latest('id')

    print(orders)
    return render(request, 'orders.html', {'orders': orders})


def cancel_order(request, order_id, cart_id):
    print(request.method)
    if request.method == "POST":
        cart = get_object_or_404(Cart, id=cart_id)
        order = get_object_or_404(Order, id=order_id)
        order.product.remove(cart)
    return redirect('order_history')


def add_to_wishlist(request, product_id):
    print(request.method)
    if request.method == "POST":
        products = Product.objects.get(id=product_id)
        wishlist, created = Wishlistitems.objects.get_or_create(
            user=request.user)
        wishlist.product.add(products)
        messages.success(request, "Added " +
                         products.title + " to your WishList")
    return redirect('view_product')


def remove_from_wishlist(request, product_id):
    print(request.method)
    if request.method == "POST":
        products = get_object_or_404(Product, id=product_id)
        wishlist = get_object_or_404(Wishlistitems, user=request.user)
        wishlist.product.remove(products)
        messages.success(request, products.title +
                         " has been removed from your WishList")
    return redirect('view_product')


@login_required
def view_wishlist(request):
    wishlist = Wishlistitems.objects.filter(user=request.user)
    return render(request, 'wishlist.html', {'wlist': wishlist})


class productapiList(ListView):

    model = Product

    def render_to_response(self, request):
        queryset = self.get_queryset()
        data = serializers.serialize("json", queryset, indent=4)
        return HttpResponse(data, content_type="application/json")


class SearchapiList(ListView):

    model = Product

    def render_to_response(self, request):
        result = self.get_queryset()
        query = self.request.GET.get('search')
        print(query)
        if query:
            postresult = Product.objects.filter(
                Q(title__icontains=query) | Q(brand__brand_name__icontains=query), in_stock=True)
            result = postresult
        data = serializers.serialize("json", result, indent=4)
        return HttpResponse(data, content_type="application/json")


class cartapiList(ListView):

    model = Cart

    def render_to_response(self, request):
        queryset = self.get_queryset()
        data = serializers.serialize("json", queryset, indent=4)
        return HttpResponse(data, content_type="application/json")


class addcartapiList(ListView):

    model = Cart

    def render_to_response(self, request):
        queryset = self.get_queryset()
        cart = queryset.filter(
            Q(user_id=self.request.user.id) & Q(is_active=True))
        data = serializers.serialize("json", cart, indent=4)
        return HttpResponse(data, content_type="application/json")


class orderapiList(ListView):

    model = Order

    def render_to_response(self, request):
        queryset = self.get_queryset()
        data = serializers.serialize("json", queryset, indent=4)
        return HttpResponse(data, content_type="application/json")


class lastorderapiList(ListView):

    model = Order

    def render_to_response(self, request):
        queryset = self.get_queryset()
        orders = queryset.latest('id')
        data = serializers.serialize("json", orders, indent=4)
        return HttpResponse(data, content_type="application/json")


class CreatecheckoutSessionView(View):
    def post(self, *args, **kwargs):
        host = self.request.get_host()
        cart = Cart.objects.filter(Q(user=self.request.user.id) & Q(is_active=True))
        grand_total = cart.aggregate(grand_total=Sum(
            F('quantity')*F('price')*0.18 + (F('quantity')*F('price'))))
        user = self.request.user
        print(user.id)
        order = Order.objects.create(user_id = user.id,status=2,total_order_price=grand_total['grand_total'])
        order.product.add(*cart)
        cart.update(is_active=False)
        print(order.id)
        for item in cart:
            product_name = item.product.title
            product_quantity = item.quantity
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'inr',
                        'unit_amount': int(grand_total['grand_total']),
                        'product_data': {
                            'name': 'mobile',
                        },
                    },
                    'quantity':1,
                }
            ],
            metadata = {
                "order_id" : order.id
            },
            mode='payment',
            success_url="http://{}{}".format(host, reverse('payment-success')),
            cancel_url="http://{}{}".format(host, reverse('payment-cancel')),
        )
        payment = Payment.objects.create(order_id = order.id,transaction_id=checkout_session['id'],payment_status=2)
        payment.save()
        print(checkout_session)
        return redirect(checkout_session.url, code=303)


def paymentsuccess(request):
    context = {
        'payment_status': 'success'
    }
    return render(request, 'orderconfirmation.html', context)


def paymentcancel(request):
    context = {
        'payment_status': 'cancel'
    }
    return render(request, 'orderconfirmation.html', context)

@csrf_exempt
def webhook_view(request):
    payload = request.body.decode('utf-8')
    event = json.loads(payload)
    print(payload)
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        sessionID = session["id"]
        print(sessionID)
        ID=session["metadata"]["order_id"]
        print(ID)
        Payment.objects.filter(transaction_id=sessionID).update(payment_status=1)
        Order.objects.filter(id=ID).update(status=1)
    elif event['type'] == 'charge.failed':
        Payment.objects.filter(transaction_id=sessionID).update(payment_status=0)
        Order.objects.filter(transaction_id=sessionID).update(status=0)
    return HttpResponse(True, status=200)