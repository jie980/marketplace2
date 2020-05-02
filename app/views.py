from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, transaction
from django.views import View
from . import forms
from .forms import registerForm
from .models import Product, CartItem, Order, Room
from django.contrib import auth
import os
from django.conf import settings
from django.http import JsonResponse


# Create your views here.
def register(request):
    content = {}
    # get name from session
    username = request.session.get('name', 'guest')
    content["username"] = username
    return render(request, "app/register.html", content)


def registered(request):
    content = {}
    # create a signup form
    form = registerForm(request.POST)
    content['form'] = form
    # get name from session
    username = request.session.get('name', 'guest')
    content["username"] = username
    captcha = request.POST.get('captcha').lower()
    # verify the captcha first
    if captcha != request.session.get('captcha'):
        content['captcha_error'] = 'Wrong verification code'
        username = request.session.get('name', 'guest')
        content["username"] = username
        return render(request, 'app/register.html', content)
    # when form is valid and captcha is correct
    elif form.is_valid() and captcha == request.session.get('captcha'):
        try:
            # try to create a new user
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'])
            # redirect to main page
            content['notice'] = "You created account! Let's login!"
            return render(request, "app/login.html", content)
        # name error
        except IntegrityError:
            form.add_error('username', 'Username is taken')
            # register again
            return render(request, 'app/register.html', content)
    else:
        # form incomplete
        return render(request, 'app/register.html', content)


def login(request):
    content = {}
    username = request.session.get('name', 'guest')
    content["username"] = username
    return render(request, "app/login.html", content)


def logined(request):
    content = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        captcha = request.POST.get('captcha').lower()
        # when there is no input
        if username == '' or password == '':
            content['login_error'] = 'Username and password cannot be empty'
            sername = request.session.get('name', 'guest')
            content["username"] = username

            return render(request, "app/login.html", content)  # register fail
        else:
            user = auth.authenticate(username=username, password=password)
            # there is record in database,and captcha is correct
            if user is not None and captcha == request.session.get('captcha'):
                request.session['name'] = username  # use session to store username
                auth.login(request, user)  # successfully logged in
                content["username"] = username
                # redirect to the main page
                return HttpResponseRedirect('/app', content)
            # when captcha is not correct, reload the page
            elif captcha != request.session.get('captcha'):
                content['captcha_error'] = 'Wrong verification code'
                username = request.session.get('name', 'guest')
                content["username"] = username
                return render(request, "app/login.html", content)
            # when there isn't record in database
            else:
                content['login_error'] = 'Wrong username or password'
                username = request.session.get('name', 'guest')
                content["username"] = username

                return render(request, "app/login.html", content)  # register fail
    return render(request, 'app/login.html')


def logout(request):
    # clear session
    # request.session.clear()
    request.session.flush()  # delete session
    return HttpResponseRedirect('/app')


def index(request):
    content = {}
    # get name from session
    username = request.session.get('name', 'guest')
    content["username"] = username
    return render(request, "app/index.html", content)


def sell(request):
    content = {}
    # get name from session
    username = request.session.get('name', 'guest')
    content["username"] = username
    return render(request, 'app/sell.html', content)


def posted(request):
    content = {}
    # fill in and upload form
    form = forms.sellForm(request.POST, request.FILES)
    if form.is_valid():
        # create an object in table
        aProduct = Product()
        aProduct.pName = form.cleaned_data['pName']
        aProduct.pDescription = form.cleaned_data['pDescription']
        # aPic = form.cleaned_data['pPicture']
        aProduct.pPrice = form.cleaned_data['pPrice']
        aProduct.pInventory = form.cleaned_data['pInventory']
        # load pic, if no pic, then None
        aPic = request.FILES.get("aPicture", None)
        if aPic != None:
            # upload pic to database
            filepath = os.path.join(settings.MEDIA_ROOT, aPic.name)
            aProduct.pPicture = filepath
            with open(filepath, 'wb') as fp:
                for info in aPic.chunks():  # upload in chunks
                    fp.write(info)
        aProduct.pOwner = request.user
        aProduct.save()
        content['posted'] = "posted success"
        return HttpResponseRedirect('/app/myaccount/myproducts')
    # form incomplete
    content['form'] = form
    username = request.session.get('name', 'guest')
    content['username'] = username
    return render(request, 'app/sell.html', content)


def myaccount(request):
    content = {}
    # get name from session
    username = request.session.get('name', 'guest')
    content["username"] = username
    return render(request, 'app/myaccount.html', content)


def myproducts(request):
    content = {}
    # get name from session
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
    # get the item
    product = Product.objects.get(pk=pid);
    # get name from session
    username = request.session.get('name', 'guest')
    content["username"] = username
    content["product"] = product
    # store the id of the current item
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
        # load pic, if no pic, None
        aPic = request.FILES.get("pPicture", None)
        if aPic != None:
            # upload pic to database
            filepath = os.path.join(settings.MEDIA_ROOT, aPic.name)
            aProduct.pPicture = filepath
            with open(filepath, 'wb') as fp:
                for info in aPic.chunks():  # upload in chunks
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
    # get name from session
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


# iddict = {}  # global variable used for storing all cartitem


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
        itemlist = request.user.cartitem_set.all().filter(isDelete=False)
        pathlist = []
        for item in itemlist:
            paths = item.product.pPicture.name
            path = paths.split('/')[-1]
            pathlist.append(path)
            # iddict[item.product.pk] = item.quantity
        ziplist = zip(itemlist, pathlist)
        # request.session['itemlist'] = ziplist

        print(ziplist)
        content['itemlist'] = ziplist
        # content['iddict'] = iddict
        # print(iddict)
    return render(request, 'app/cart.html', content)


# delete item
def deletecart(request):
    content = {}
    pid = request.GET.get('pid')
    cartItem = CartItem.objects.get(pk=pid)
    productid = cartItem.product.pk
    print(productid)
    # del iddict[productid]
    cartItem.delete()

    # print(iddict)
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
        # iddict[productid] = iddict[productid] + 1
        # print(iddict)
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
        # iddict[productid] = iddict[productid] - 1
        # print(iddict)
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
    # get name from session
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

        itemlist = request.user.cartitem_set.all().filter(isDelete=False)
        print(itemlist)
        for item in itemlist:
            print(item.isDelete)
            # change the inventory
            product = item.product
            product.pInventory = product.pInventory - item.quantity
            product.save()
            # remove everything from the his/her cart and also the cart in the database
            if item.isDelete == False:
                item.isDelete = True
                # add item into the order
                item.orderid = aOrder
                item.save()

        content['order'] = aOrder
        if aOrder.pay == "paypal":
            return render(request, "app/paypal.html", content)
        else:
            return render(request, "app/cod.html", content)

    else:
        # form incomplete
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


def chat_index(request):
    return render(request, 'app/chat_index.html', {})


def room(request, room_name=None):
    return render(request, 'app/room.html', {
        'room_name': room_name,

    })


# verification code generator
def captcha(request):
    from PIL import Image, ImageDraw, ImageFont
    import random

    bgcolor = (random.randrange(20, 100), random.randrange(20, 100), random.randrange(20, 100))

    size = (100, 50)
    # create a new canvas
    aImage = Image.new("RGB", size, bgcolor)
    # create a new pen
    aPen = ImageDraw.Draw(aImage)
    # candidate for the captcha
    str = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    selectedstr = ''
    for i in range(0, 4):
        selectedstr += str[random.randrange(0, len(str))]
    print(selectedstr)

    font = ImageFont.truetype("static/fonts/helveticaneue_medium-webfont.ttf", 30)

    ftcolor = (225, random.randrange(0, 255), random.randrange(0, 255))

    aPen.text((5, random.randrange(3, 7)), selectedstr[0], font=font, fill=ftcolor)
    aPen.text((30, random.randrange(3, 7)), selectedstr[1], font=font, fill=ftcolor)
    aPen.text((55, random.randrange(3, 7)), selectedstr[2], font=font, fill=ftcolor)
    aPen.text((75, random.randrange(3, 7)), selectedstr[3], font=font, fill=ftcolor)

    # make two horizon lines in the canvas
    linefill = (random.randrange(0, 255), random.randrange(0, 255), 255)
    aPen.line((0, random.randrange(10, 40), 100, random.randrange(10, 40)), fill=linefill, width=2)
    linefill2 = (random.randrange(0, 255), random.randrange(0, 255), 255)
    aPen.line((0, random.randrange(10, 40), 100, random.randrange(10, 40)), fill=linefill2, width=2)
    # make 200 pts in the canvas
    for i in range(0, 200):
        # xy is the postion to point
        xy = (random.randrange(0, 100), random.randrange(0, 50))
        # fill with ramdom color
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        aPen.point(xy, fill=fill)
    del aPen
    # use session to store the captcha
    request.session['captcha'] = selectedstr.lower()
    import io
    buffer = io.BytesIO()
    aImage.save(buffer, 'png')

    return HttpResponse(buffer.getvalue(), 'image/png')
