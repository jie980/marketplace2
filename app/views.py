from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, transaction
from . import forms
from .models import Product, CartItem, Order, Room
from django.contrib import auth
import os
from django.conf import settings
from django.http import JsonResponse
import haikunator
import random
import string

# Create your views here.
def register(request):
    content = {}
    # 获取session里的name
    username = request.session.get('name', 'guest')
    content["username"] = username
    return render(request, "app/register.html", content)


def registered(request):
    content = {}
    # create a signup form
    form = forms.registerForm(request.POST)
    content['form'] = form
    # 获取session里的name
    username = request.session.get('name', 'guest')
    content["username"] = username
    if form.is_valid():
        try:
            # try to create a new user
            user = User.objects.create_user(
                form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'])
            # 转到主页稍后修改
            content['notice'] = "You created account! Let's login!"
            return render(request, "app/login.html", content)
        # 重名错误
        except IntegrityError:
            form.add_error('username', 'Username is taken')
            # 重新注册
            return render(request, 'app/register.html', content)
    else:
        # form不完整
        return render(request, 'app/register.html', content)


def login(request):
    content = {}
    username = request.session.get('name', 'guest')
    content["username"] = username
    return render(request, "app/login.html", content)


def logined(request):
    content = {}
    if request.method == 'POST':
        # 直接获取
        username = request.POST.get('username')
        password = request.POST.get('password')
        # 用户认证
        user = auth.authenticate(username=username, password=password)
        # 数据库里有记录
        if user is not None:
            request.session['name'] = username  # 用session来储存username
            auth.login(request, user)  # 登陆成功
            content["username"] = username
            # 切换到主页
            return HttpResponseRedirect('/app', content)
        # 数据库里无记录
        else:
            content['login_error'] = 'Wrong username or password'
            username = request.session.get('name', 'guest')
            content["username"] = username
            return render(request, "app/login.html", content)  # 注册失败
    return render(request, 'app/login.html')


def logout(request):
    # 清除session
    # request.session.clear()
    request.session.flush()  # 删除当前会话和当前session
    return HttpResponseRedirect('/app')


def index(request):
    content = {}
    # 获取session里的name
    username = request.session.get('name', 'guest')
    content["username"] = username
    return render(request, "app/index.html", content)


def sell(request):
    content = {}
    # 获取session里的name
    username = request.session.get('name', 'guest')
    content["username"] = username
    return render(request, 'app/sell.html', content)


def posted(request):
    content = {}
    # aProduct = Product()
    # aProduct.pName='soccer'
    # aProduct.pDescription = 'nice football'
    # aProduct.pPrice = 12
    # aProduct.pInventory=3
    # aProduct.save()
    # 填写上传form
    form = forms.sellForm(request.POST, request.FILES)
    if form.is_valid():
        # 创建一个数据库object
        aProduct = Product()
        aProduct.pName = form.cleaned_data['pName']
        aProduct.pDescription = form.cleaned_data['pDescription']
        # aPic = form.cleaned_data['pPicture']
        aProduct.pPrice = form.cleaned_data['pPrice']
        aProduct.pInventory = form.cleaned_data['pInventory']
        # 读取图片，没图片就是None
        aPic = request.FILES.get("aPicture", None)
        if aPic != None:
            # 上传图片地址到数据库
            filepath = os.path.join(settings.MEDIA_ROOT, aPic.name)
            aProduct.pPicture = filepath
            with open(filepath, 'wb') as fp:
                for info in aPic.chunks():  # 分段上传
                    fp.write(info)
        aProduct.pOwner = request.user
        aProduct.save()
        content['posted'] = "posted success"
        return HttpResponseRedirect('/app/myaccount/myproducts')
    # 表单不完整
    content['form'] = form
    username = request.session.get('name', 'guest')
    content['username'] = username
    return render(request, 'app/sell.html', content)


def myaccount(request):
    content = {}
    # 获取session里的name
    username = request.session.get('name', 'guest')
    content["username"] = username
    return render(request, 'app/myaccount.html', content)


def myproducts(request):
    content = {}
    # 获取session里的name
    username = request.session.get('name', 'guest')
    content["username"] = username
    if request.user.is_authenticated:
        plist = request.user.product_set.all()
        pathlist = []
        for p in plist:
            pPath = p.pPicture.name
            chunk = pPath.split('/')
            showpath = chunk[-1]
            pathlist.append(showpath)
        ziplist = zip(plist, pathlist)
        content['plist'] = ziplist

    else:
        content['notice'] = "You need to login!"
    return render(request, 'app/myproducts.html', content)


def edit(request, pid):
    content = {}
    # 获取当前物品
    product = Product.objects.get(pk=pid);
    # 获取session里的name
    username = request.session.get('name', 'guest')
    content["username"] = username
    content["product"] = product
    # 保存当前物品的id
    request.session['pid'] = product.pk
    print(request.session.get('pid'))
    return render(request, 'app/edit.html', content)


def edited(request):
    content = {}
    cur_pid = request.session.get('pid')
    aProduct = Product.objects.get(pk=cur_pid)
    form = forms.sellForm(request.POST, request.FILES)
    if form.is_valid():
        aProduct.pName = form.cleaned_data['pName']
        aProduct.pDescription = form.cleaned_data['pDescription']
        # aPic = form.cleaned_data['pPicture']
        aProduct.pPrice = form.cleaned_data['pPrice']
        aProduct.pInventory = form.cleaned_data['pInventory']
        # 读取图片，没图片就是None
        aPic = request.FILES.get("pPicture", None)
        if aPic != None:
            # 上传图片地址到数据库
            filepath = os.path.join(settings.MEDIA_ROOT, aPic.name)
            aProduct.pPicture = filepath
            with open(filepath, 'wb') as fp:
                for info in aPic.chunks():  # 分段上传
                    fp.write(info)
        aProduct.pOwner = request.user
        aProduct.save()
        content['posted'] = "posted success"
        return HttpResponseRedirect('/app/myaccount/myproducts')
    content['form'] = form
    username = request.session.get('name', 'guest')
    content['username'] = username
    content["product"] = aProduct
    return render(request, 'app/edit.html', content)


def deleted(request, pid):
    content = {}
    product = Product.objects.get(pk=pid)
    product.delete()
    return HttpResponseRedirect('/app/myaccount/myproducts')


def shop(request):
    content = {}
    # 获取session里的name
    username = request.session.get('name', 'guest')
    content["username"] = username

    plist = Product.objects.all()

    pathlist = []
    for p in plist:
        pPath = p.pPicture.name
        chunk = pPath.split('/')
        showpath = chunk[-1]
        pathlist.append(showpath)
    ziplist = zip(plist, pathlist)
    content['plist'] = ziplist
    return render(request, 'app/shop.html', content)


def productdetail(request, pid):
    content = {}
    username = request.session.get('name', 'guest')
    content["username"] = username

    product = Product.objects.get(pk=pid)
    content['product'] = product
    paths = product.pPicture.name.split('/')
    path = paths[-1]
    content['pPath'] = path

    return render(request, 'app/productDetails.html', content)


iddict = {}  # global variable used for all cart and checkout method


def cart(request):
    content = {}
    username = request.session.get('name', 'guest')
    content["username"] = username
    # if user add new item into cart
    if request.method == 'POST':
        print("--------------------------------------------------------------")
        pid = request.POST.get('pid')
        product = Product.objects.get(pk=pid)
        quantity = request.POST.get('quantity')
        price = product.pPrice

        buyer = request.user
        # item already exists in cart
        try:
            owner = User.objects.get(id=1)
            # create a dummy order for allowing every cartitem has a default order
            Order.objects.get_or_create(firstname="dummy", lastname="dummy", companyname="dummy", address="dummy",
                                        zipcode="dummy", phone=1, pay="paypal", price=1, owner=owner)

            item = CartItem.objects.get(product=product, buyer=buyer, isDelete=False)
            item.quantity = item.quantity + int(quantity)
            item.save()
            print(item)
        except:
            # item does not exist

            item = CartItem()
            item.buyer = buyer
            item.product = product
            item.price = price
            item.quantity = quantity
            item.orderid = Order.objects.get(pk=1)  # dummy order just let each item has an order
            item.save()

    # if user check his/her cart, show all of them
    if request.user.is_authenticated:
        # 修改了
        itemlist = request.user.cartitem_set.all().filter(isDelete=False)

        pathlist = []
        for item in itemlist:
            paths = item.product.pPicture.name
            path = paths.split('/')[-1]
            pathlist.append(path)
            iddict[item.product.pk] = item.quantity
        ziplist = zip(itemlist, pathlist)
        # request.session['itemlist'] = ziplist

        print(ziplist)
        content['itemlist'] = ziplist
        content['iddict'] = iddict
        print(iddict)
    return render(request, 'app/cart.html', content)


# delete item
def deletecart(request):
    content = {}
    pid = request.GET.get('pid')
    cartItem = CartItem.objects.get(pk=pid)
    productid = cartItem.product.pk
    print(productid)
    del iddict[productid]
    cartItem.delete()

    print(iddict)
    data = {}
    data['pid'] = pid

    return JsonResponse(data)


# plus item
def editcart(request):
    pid = request.GET.get('pid')

    cartItem = CartItem.objects.get(pk=pid)
    # use can buy item iff enough Inventory
    if cartItem.quantity < cartItem.product.pInventory:
        cartItem.quantity = cartItem.quantity + 1
        cartItem.save()
        productid = cartItem.product.pk
        iddict[productid] = iddict[productid] + 1
        print(iddict)
        data = {}
        data['pid'] = pid
        return JsonResponse(data)
    else:
        data = {}
        data['pid'] = pid
        return JsonResponse(data)


# minus item
def editcart2(request):
    pid = request.GET.get('pid')
    cartItem = CartItem.objects.get(pk=pid)
    # the number of item buy cannot be less than 1
    if cartItem.quantity > 1:
        cartItem.quantity = cartItem.quantity - 1
        cartItem.save()

        productid = cartItem.product.pk
        iddict[productid] = iddict[productid] - 1
        print(iddict)
        data = {}
        data['pid'] = pid
        return JsonResponse(data)
    else:
        data = {}
        data['pid'] = pid
        return JsonResponse(data)


def checkout(request):
    content = {}
    form = forms.checkoutForm(request.POST)
    # request.session['form'] = form
    # 获取session里的name

    username = request.session.get('name', 'guest')
    content["username"] = username
    if form.is_valid():
        # create the order
        aOrder = Order()
        aOrder.firstname = form.cleaned_data['firstname']
        aOrder.lastname = form.cleaned_data['lastname']
        aOrder.companyname = form.cleaned_data['companyname']
        aOrder.country = form.cleaned_data['country']
        aOrder.address = form.cleaned_data['address']
        aOrder.city = form.cleaned_data['city']
        aOrder.zipcode = form.cleaned_data['zipcode']
        aOrder.phone = form.cleaned_data['phone']
        aOrder.comment = form.cleaned_data['comment']
        aOrder.price = request.POST.get('price')
        aOrder.pay = request.POST.get('paymethod')
        aOrder.owner = request.user
        aOrder.save()

        # #change the inventory
        for pid, amt in iddict.items():
            product = Product.objects.get(pk=pid)

            product.pInventory = product.pInventory - amt
            product.save()
        # remove everything from the his/her cart and also the cart in the database
        # add item into the order
        itemlist = request.user.cartitem_set.all()
        print(itemlist)
        for item in itemlist:
            print(item.isDelete)

            if item.isDelete == False:
                item.isDelete = True
                item.orderid = aOrder
                item.save()

        content['order'] = aOrder
        if aOrder.pay == "paypal":
            return render(request, "app/paypal.html", content)
        else:
            return render(request, "app/cod.html", content)

    else:
        # form不完整
        content['order'] = "Order fail! Please refresh to see your item"
        content['form'] = form
        return render(request, "app/cart.html", content)


def orderhistory(request):
    content = {}
    orderlist = request.user.order_set.all()
    orderlist = orderlist.filter(pk__gt=1)  # except the dummy order
    orderlist2 = []
    print(orderlist)
    username = request.session.get('name', 'guest')
    content["username"] = username
    content['orderlist'] = orderlist
    for order in orderlist:
        itemlist = order.cartitem_set.all()
        print(order.pk, ":", itemlist)
        orderlist2.append(itemlist)

    # pass all the order into content
    content['orderlist'] = zip(orderlist, orderlist2)

    return render(request, "app/orderHistory.html", content)

# def new_room(request):
#     """
#     Randomly create a new room, and redirect to it.
#     """
#     new_room = None
#     while not new_room:
#         with transaction.atomic():
#             label = haikunator.haikunate()
#             # if Room.objects.filter(label=label).exists():
#             #     continue
#             #new_room = Room.objects.create(label=label)
#     return redirect(chat_room, label=label)
#
# def chat_room(request, label):
#     """
#     Room view - show the room, with latest messages.
#
#     The template for this view has the WebSocket business to send and stream
#     messages, so see the template for where the magic happens.
#     """
#     # If the room with the given label doesn't exist, automatically create it
#     # upon first visit (a la etherpad).
#     room, created = Room.objects.get_or_create(label=label)
#
#     # We want to show the last 50 messages, ordered most-recent-last
#     messages = reversed(room.messages.order_by('-timestamp')[:50])
#
#     return render(request, "app/room.html", {
#         'room': room,
#         'messages': messages,
#     })
def room(request, room_name=None):
    return render(request, 'app/room.html', {
        'room_name': room_name
    })