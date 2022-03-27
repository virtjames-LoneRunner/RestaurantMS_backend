from dataclasses import field
from rest_framework import serializers
from .models import Categories, InventoryItems, MenuItems, Users


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('id', 'role', 'name', 'email', 'password', 'created_at', 'updated_at')

class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ('id', 'code', 'category')

class MenuItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItems 
        fields = ('id', 'category', 'available', 'menu_item', 'unit', 'unit_price', 'created_at', 'updated_at')

class InventoryItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryItems
        fields = ('id', 'inventory_item', 'quantity', 'unit', 'created_at', 'updated_at')