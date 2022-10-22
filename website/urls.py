from django.urls import path
from website import views
from django.urls import include, re_path as url

urlpatterns = [
    path('login/',views.login_request,name='login'),
    path('logout/',views.logout_request,name='logout'),
    path('index/',views.index,name='index'),
    path('view/',views.ProductListview.as_view(),name='view'),
    path('search/',views.SearchView.as_view(),name='search'),
    path('cart/',views.cart_detail,name='cart'),
    url(r'^add/(?P<product_id>\d+)/$', views.add_to_cart, name='add_to_cart'),
    #path('remove_cart/<int:product_id>',views.remove_cart,name='remove_cart'),
]