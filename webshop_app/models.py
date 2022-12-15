import uuid as uuid

from datetime import datetime
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

from django_countries.fields import CountryField


class Profile(models.Model):
    """ Extends auth.User model. """
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    birth_date = models.DateField()

    def __str__(self):
        return str(self.user)


class Address(models.Model):
    """ Model for addresses. One user can store many addresses. """
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    country = CountryField(null=True)
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Category(models.Model):
    """ Category model. """
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.category


class Product(models.Model):
    """ Product model. Belongs to specific category. """
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product = models.CharField(max_length=100)
    description = models.TextField(null=True)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    picture = models.ImageField(upload_to='staticfiles/images/', null=True, blank=True)
    available = models.BooleanField(default=True, null=False)

    def __str__(self):
        return self.product


class Cart(models.Model):
    """ Cart model. Stores products for further actions. """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)


class Order(models.Model):
    """ Order model. """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cart = models.ManyToManyField(Cart)
    order_id = models.UUIDField(default=uuid.uuid4, unique=True, db_index=True, editable=False)
    order_date = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return str(self.user)


class Comment(models.Model):
    """ Comment model. """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    text = models.TextField()
    text_date = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return str(self.user)
