from django.urls import path
from website import views
from django.urls import include, re_path as url

urlpatterns = [

    path('index/',views.index,name='index'),

    path('view_product/',views.product_view,name='view_product'),
    

    path('search/',views.SearchView.as_view(),name='search'),

    path('cart/',views.cart_detail,name='cart'),
    path('add_cart/<product_id>', views.add_to_cart, name='add_to_cart'),
    path('remove_cart/<cart_id>',views.remove_cart,name='remove_cart'),
    path('remove_item_cart/<product_id>', views.remove_item_cart, name='remove_item_cart'),

    path('orderplaced/',views.order_placed,name='orderplaced'),
    path('order_history/',views.order_history,name='order_history'),
    path('cancel_order/<order_id>/<cart_id>/',views.cancel_order,name='cancel_order'),

    path('add_wishlist/<product_id>', views.add_to_wishlist, name='add_to_wishlist'),
    path('view_wishlist/',views.view_wishlist,name='wishlist'),
    path('remove_wishlist/<product_id>',views.remove_from_wishlist,name='remove_wish'),
    
    path('productlist/',views.productList.as_view(),name='productlist'),
    path('searchlist/',views.SearchList.as_view(),name='searchlist'),
    path('cartlist/',views.cartList.as_view(),name='cartlist'),
    path('addcartlist/',views.addcartList.as_view(),name='addcartlist'),
    path('orderlist/',views.orderList.as_view(),name='orderlist'),
    path('lastorderlist/',views.lastorderList.as_view(),name='lastorderlist'),
    
]