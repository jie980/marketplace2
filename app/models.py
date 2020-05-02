from __future__ import unicode_literals
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Product(models.Model):
    pName = models.CharField(max_length=20)
    pDescription = models.CharField(max_length=1000)
    pPicture = models.FileField(upload_to='./static')
    pPrice = models.DecimalField(max_digits=7, decimal_places=2)
    pInventory = models.IntegerField()
    pOwner = models.ForeignKey(User, on_delete=models.CASCADE)


class Order(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    firstname = models.CharField(max_length=20)
    lastname = models.CharField(max_length=20)
    companyname = models.CharField(max_length=100)
    country = models.CharField(max_length=20)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=20)
    zipcode = models.CharField(max_length=10)
    phone = models.IntegerField()
    comment = models.CharField(max_length=1000)
    pay = models.CharField(max_length=10)


class CartItem(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    quantity = models.IntegerField()
    isDelete = models.BooleanField(default=False)
    orderid = models.ForeignKey(Order, on_delete=models.CASCADE)


class Room(models.Model):

    userOne = models.CharField(max_length=30, null=True)
    userTwo = models.CharField(max_length=30, null=True)
    content = models.TextField(blank=True)

    def __str__(self):
        return self.userTwo
