from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Category(models.Model):

    DoesExist = True

    class Meta:
        ordering = ['category_id']

    category_id = models.IntegerField(primary_key=True)
    category_name = models.fields.TextField(max_length=1000, null=True)
    category_url = models.fields.TextField(max_length=1000, null=True)


class Product(models.Model):
    class Meta:
        ordering = ['product_id']

    category_id = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    product_id = models.IntegerField(primary_key=True)
    product_name = models.fields.TextField(max_length=1000, null=True)
    product_image = models.fields.TextField(max_length=1000, null=True)
    product_url = models.fields.TextField(max_length=1000, null=True)
    product_ingredients = models.fields.TextField(max_length=1000, null=True)
    product_nutriscore = models.fields.TextField(max_length=1000)


class Favourite(models.Model):

    class Meta:
        ordering = ['substitute_id']

    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    substitute_id = models.AutoField(primary_key=True)
    substitute_name = models.fields.TextField(max_length=1000, null=True)
    substitute_image = models.fields.TextField(max_length=1000, null=True)
    substitute_nutriscore = models.fields.CharField(max_length=1000)
