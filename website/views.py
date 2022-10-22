from django.http import HttpResponse
from django.shortcuts import render, redirect
from website.models import Product, cart
from website.forms import productForm
from django.views.generic.list import ListView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist


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
        carts = cart.objects.filter(user=user)
        amount = 0.0
        cart_product = [p for p in cart.objects.all() if p.user == user]
        print(cart_product)
        if cart_product:
            for p in cart_product:
                total_price = (p.quantity * p.price)
                print(total_price)
                amount += total_price
                print(amount)
        context = {'form':carts,'amount':amount,}
        return render(request,'cart.html',context)

def add_to_cart(request,product_id):
       user = request.user
       product = Product.objects.get(id=product_id)
       cart(user=user, product=product).save()
       return redirect('cart')


