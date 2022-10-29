from django.urls import path
from website import views
from django.urls import include, re_path as url

urlpatterns = [

    path('login/',views.login_request,name='login'),
    path('logout/',views.logout_request,name='logout'),
    path('index/',views.index,name='index'),
    path('view_p/',views.view,name='view_p'),
    path('search/',views.SearchView.as_view(),name='search'),
    path('cart/',views.cart_detail,name='cart'),
    url(r'^add/(?P<id>\d+)/$', views.add_to_cart, name='add_to_cart'),
    path('remove_cart/<id>',views.remove_cart,name='remove_cart'),
    path('orderplaced/',views.orderplaced,name='orderplaced'),
    path('cancel_order/',views.cancel_order,name='cancel_order'),
    path('remove_item_cart/<id>', views.remove_item_cart, name='remove_item_cart'),
    url(r'^add_wishlist/(?P<id>\d+)/$', views.add_to_wishlist, name='add_to_wishlist'),
    path('view_wishlist/',views.view_wishlist,name='wishlist'),
    path('remove_wishlist/<id>',views.remove_from_wishlist,name='remove_wish'),
    

]