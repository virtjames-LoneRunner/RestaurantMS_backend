from django.db import models

# Create your models here.
class Users(models.Model):
    role = models.CharField(max_length=20)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Categories(models.Model):
    code = models.CharField(max_length=10)
    category = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return f'Category: {self.category}'

class MenuItems(models.Model):
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    available = models.BooleanField(default=True)
    menu_item = models.CharField(max_length=100)
    unit = models.CharField(max_length=20)
    unit_price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.menu_item

class Ingredients(models.Model):
    menu_item = models.ForeignKey(MenuItems, on_delete=models.CASCADE, blank=True)
    item_id = models.IntegerField()
    item = models.CharField(max_length=255)
    unit = models.CharField(max_length=20)
    quantity = models.FloatField()

class InventoryItems(models.Model):
    inventory_item = models.CharField(max_length=255)
    item_category = models.CharField(max_length=255)
    quantity = models.FloatField()
    reorder_quantity = models.FloatField()
    unit = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Transactions(models.Model):
    cashier_id = models.CharField(max_length=10)
    transaction_id = models.CharField(max_length=50)
    transaction_type = models.CharField(max_length=50)
    transaction_date = models.DateTimeField(auto_now_add=True)
    table_number = models.IntegerField()
    
    total_amount = models.FloatField()
    amount_given = models.FloatField()
    discount = models.FloatField()
    change = models.FloatField()

    address = models.CharField(max_length=255)

    items = models.ManyToManyField(MenuItems, through="TransactionItems", through_fields=('transaction', 'item'))



class TransactionItems(models.Model):
    transaction = models.ForeignKey(Transactions, on_delete=models.CASCADE)
    item = models.ForeignKey(MenuItems, on_delete=models.DO_NOTHING)

class OrderItems(models.Model):
    transaction_id = models.ForeignKey(Transactions, on_delete=models.CASCADE)
    item = models.CharField(max_length=100)
    unit_price = models.FloatField()
    unit = models.CharField(max_length=20)
    pcs = models.IntegerField()
