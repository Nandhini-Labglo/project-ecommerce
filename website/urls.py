from django.urls import path
from website import views
from django.urls import include, re_path as url

urlpatterns = [

    path('login/',views.login_request,name='login'),
    path('logout/',views.logout_request,name='logout'),
    path('index/',views.index,name='index'),
    path('view_p/',views.view,name='view_p'),
    #path('view/',views.ProductListview.as_view(),name='view'),
    path('search/',views.SearchView.as_view(),name='search'),
    path('cart/',views.cart_detail,name='cart'),
    url(r'^add/(?P<id>\d+)/$', views.add_to_cart, name='add_to_cart'),
    #url(r'^remove/(?P<product_id>\d+)/$', views.remove, name='remove'),
    path('remove_cart/<id>',views.remove_cart,name='remove_cart'),
    path('orderplaced/',views.orderplaced,name='orderplaced'),
    path('order/',views.order,name='order'),
    path('remove_item_cart/<id>', views.remove_item_cart, name='remove_item_cart'),
    url(r'^add_wishlist/(?P<id>\d+)/$', views.add_to_wishlist, name='add_to_wishlist'),
    path('view_wishlist/',views.view_wishlist,name='wishlist'),
    #path('minus_cart/', views.minus_cart, name='minus_cart'),

]