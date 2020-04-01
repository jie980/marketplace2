from django.conf.urls import url
from django.urls import path, re_path
import app.views


#进行匹配view
urlpatterns = [
    path('register/',app.views.register,name='register'),
    path('registered/',app.views.registered),
    path('login/',app.views.login,name='login'),
    path('logined/',app.views.logined),
    path('logout/',app.views.logout,name='logout'),
    path('',app.views.index,name='index'),
    path('myaccount/',app.views.myaccount,name='myaccount'),
    path('myaccount/myproducts/',app.views.myproducts,name='myproducts'),
    path('myaccount/myproducts/sell/',app.views.sell,name='sell'),
    path('myaccount/myproducts/posted/',app.views.posted,name='posted'),
    path('myaccount/myproducts/edit/<int:pid>/',app.views.edit),
    path('myaccount/myproducts/edited/',app.views.edited,name='edited'),
    path('myaccount/myproducts/deleted/<int:pid>/',app.views.deleted),
    path('myaccount/orderhistory/',app.views.orderhistory,name='orderhistory'),
    path('shop/',app.views.shop,name='shop'),
    path('shop/<int:pid>/',app.views.productdetail,name='detail'),
    path('cart/',app.views.cart,name='cart'),
    path('cart/edit1/',app.views.editcart,name='editcart'),
    path('cart/edit2/',app.views.editcart2,name='editcart2'),
    path('cart/delete/',app.views.deletecart),
    path('checkout/',app.views.checkout,name='checkout'),
    path('room/',app.views.room,name='room'),
]