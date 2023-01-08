import os.path
import re

from django.db import models
from django.urls import reverse
from django.utils.text import slugify


# Create your models here.


def upload_image_to(instance, filename):
    return os.path.join(instance.category.name.lower(), filename)


def create_slug(string):
    string = re.sub(r'[^\w\s]', '', string).lower()
    return slugify(string)


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, unique=True)
    slug = models.CharField(max_length=100, db_index=True, unique=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = create_slug(self.name)
        super().save(*args, **kwargs)

    # def get_absolute_url(self):
    #     return reverse('category_view', args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=False)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=100, db_index=True, unique=True)
    vendor_code = models.CharField(max_length=100, db_index=True, unique=True)
    image = models.ImageField(upload_to=upload_image_to, blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = create_slug(self.vendor_code)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.image.delete()
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)

    # def get_absolute_url(self):
    #     return reverse('product_view', args=[self.category.slug, self.slug])
