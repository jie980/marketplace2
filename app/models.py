from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
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


# class Meta:
# unique_together = (('buyer', 'product', 'isDelete'),)


# class Cart(object):

#     def __init__(self, *args, **kwargs):
#     	self.items = []
#     	self.total_price = 0
#     def add_product(self,product):
#     	self.total_price += product.pPrice
#     	for item in self.items:
#     		if item.product.id == product.id:
#     			item.quantity += 1
#     	return self.items.append(CartItem(product=product,unit_price=product.price,quantity=1))

#      jane- model for storage of chat history


class Room(models.Model):
    name = models.TextField()
    label = models.SlugField(unique=True)

    def __unicode__(self):
        return self.label


class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    handle = models.TextField()
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)

    def __unicode__(self):
        return '[{timestamp}] {handle}: {message}'.format(**self.as_dict())

    @property
    def formatted_timestamp(self):
        return self.timestamp.strftime('%b %-d %-I:%M %p')

    def as_dict(self):
        return {'handle': self.handle, 'message': self.message, 'timestamp': self.formatted_timestamp}