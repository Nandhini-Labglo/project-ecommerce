from django.urls import path
from website import views
from django.urls import include, re_path as url

urlpatterns = [
    #index
    path('index/',views.index,name='index'),

    #productlist
    path('view_product/',views.product_view,name='view_product'),
    
    #search
    path('search/',views.SearchView.as_view(),name='search'),

    #carts
    path('cart/',views.cart_detail,name='cart'),
    path('add_cart/<product_id>', views.add_to_cart, name='add_to_cart'),
    path('remove_cart/<cart_id>',views.remove_cart,name='remove_cart'),
    path('remove_item_cart/<product_id>', views.remove_item_cart, name='remove_item_cart'),

    #orders
    path('orderplaced/',views.order_placed,name='orderplaced'),
    path('order_history/',views.order_history,name='order_history'),
    path('cancel_order/<order_id>/<cart_id>/',views.cancel_order,name='cancel_order'),

    #wishlist
    path('add_wishlist/<product_id>', views.add_to_wishlist, name='add_to_wishlist'),
    path('view_wishlist/',views.view_wishlist,name='wishlist'),
    path('remove_wishlist/<product_id>',views.remove_from_wishlist,name='remove_wish'),
    
    #api
    path('productlist/',views.productapiList.as_view(),name='productlist'),
    path('searchlist/',views.SearchapiList.as_view(),name='searchlist'),
    path('cartlist/',views.cartapiList.as_view(),name='cartlist'),
    path('addcartlist/',views.addcartapiList.as_view(),name='addcartlist'),
    path('orderlist/',views.orderapiList.as_view(),name='orderlist'),
    path('lastorderlist/',views.lastorderapiList.as_view(),name='lastorderlist'),

    path('create-checkout-session/',views.CreatecheckoutSessionView.as_view(),name='create-checkout-session'),
    path('payment-success/',views.paymentsuccess,name='payment-success'), 
    path('payment-cancel/',views.paymentcancel,name='payment-cancel'),  
    path('webhook/',views.webhook_view,name='webhook_view'),
]