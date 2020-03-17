from django.db import models
import random, string
from django.conf import settings
from django.shortcuts import reverse
from django.db.models.signals import pre_save
from django.template.defaultfilters import slugify

# Create your models here.
CONDITION = (
    ('G', 'Good'),
    ('N', 'Normal'),
    ('B', 'Bad')
)

LABEL_CONDITION = (
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger')
)

CATEGORIES = (
    ('P', 'Phones'),
    ('EA', 'Electronics & Appliances'),
    ('F', 'Fashion'),
    ('B', 'Books'),
    ('C', 'Cars'),
    ('BK', 'Bikes'),
    ('FR', 'Furniture'),
    ('OT', 'Other'),
)


class Products(models.Model):
    name = models.CharField(max_length=40)
    brand = models.CharField(max_length=25)
    price = models.PositiveIntegerField()
    category = models.CharField(choices=CATEGORIES, max_length=2)
    description = models.TextField(max_length=250, blank=True)
    condition = models.CharField(choices=CONDITION, max_length=1)
    label = models.CharField(choices=LABEL_CONDITION, max_length=1)
    datetime = models.DateTimeField(auto_now_add=True, blank=True)
    slug = models.SlugField(max_length=150, allow_unicode=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('main:product-detail', kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse('main:add-to-cart', kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse('main:remove-from-cart', kwargs={
            'slug': self.slug
        })


def slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        slug_str = '%s-%s-%s-%s' % (instance.category, instance.brand, instance.name, instance.datetime)
        instance.slug = slugify(slug_str)


pre_save.connect(slug_generator, sender=Products)


class OrderProduct(models.Model):
    item = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.quantity} of {self.item} brought by {self.user}"


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item = models.ManyToManyField(OrderProduct)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}"
