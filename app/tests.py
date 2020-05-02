from django.test import TestCase
from .forms import sellForm
from .models import Product, Order
from django.contrib.auth.models import User
from decimal import Decimal


class TestForms(TestCase):
    def test_sellform_valid(self):
        form = sellForm(data={
            'pName': 'apple',
            'pPrice': 100.1,
            'pInventory': 10
        })

        self.assertTrue(form.is_valid())

    def test_sellform_negativeprice(self):
        form = sellForm(data={
            'pName': 'apple2',
            'pPrice': -100.11,
            'pInventory': 10
        })

        self.assertFalse(form.is_valid())

    def test_sellform_negativestock(self):
        form = sellForm(data={
            'pName': 'apple2',
            'pPrice': 100.11,
            'pInventory': -10
        })
        self.assertFalse(form.is_valid())

    def test_sellform_invalid(self):
        form = sellForm(data={
            'pName': 'apple2',
            'pInventory': 10
        })
        self.assertFalse(form.is_valid())


class productModelTest(TestCase):

    def test_product_model_equal(self):
        user = User.objects.create_user(username='kehan', email='kehan@gmail.com', password='123456')
        Product.objects.create(
            pName='apple', pDescription='It is a nice apple', pPrice=11.21,
            pInventory=99, pOwner=user)

        result = Product.objects.get(pName='apple')
        self.assertEqual(result.pPrice, Decimal('11.21'))
        self.assertEqual(result.pDescription, 'It is a nice apple')
        self.assertEqual(result.pInventory, 99)
        self.assertEqual(result.pOwner, user)


class OrderModelTest(TestCase):
    def test_cartItem_model_equal(self):
        powner = User.objects.create_user(username='kehan', email='kehan@gmail.com', password='123456')
        result = Order.objects.create(
            owner=powner, price=45.11, firstname='Ku', lastname='Kun',
            country='Canada', address='rue peel', city='montreal',
            zipcode='H3A000', phone='5141122345', pay='paypal')
        self.assertEqual(result.owner, powner)
        self.assertEqual(result.price, 45.11)
        self.assertEqual(result.firstname, 'Ku')
        self.assertEqual(result.lastname, 'Kun')
        self.assertEqual(result.country, 'Canada')
        self.assertEqual(result.address, 'rue peel')
        self.assertEqual(result.city, 'montreal')
        self.assertEqual(result.zipcode, 'H3A000')
        self.assertEqual(result.phone, '5141122345')
        self.assertEqual(result.pay, 'paypal')
