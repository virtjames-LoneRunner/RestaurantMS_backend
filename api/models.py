from django.db import models

# Create your models here.
class Users(models.Model):
    role = models.CharField(max_length=20)
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Categories(models.Model):
    code = models.CharField(max_length=10)
    category = models.CharField(max_length=100)
    
    def __str__(self):
        return f'Category: {self.category}'

class MenuItems(models.Model):
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    available = models.BooleanField(default=True)
    menu_item = models.CharField(max_length=100)
    unit = models.CharField(max_length=10)
    unit_price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.menu_item

class InventoryItems(models.Model):
    inventory_item = models.CharField(max_length=255)
    quantity = models.FloatField()
    unit = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
