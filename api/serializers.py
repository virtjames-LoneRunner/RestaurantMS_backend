from dataclasses import field
from rest_framework import serializers
from .models import Categories, Ingredients, InventoryItems, MenuItems, OrderItems, Reservations, Tables, Users, Transactions, TransactionItems


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('id', 'role', 'name', 'email', 'password', 'created_at', 'updated_at')

class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ('id', 'code', 'category')

class IngredientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredients
        fields = ('id', 'menu_item', 'item_id', 'item', 'unit', 'quantity') 

class MenuItemsSerializer(serializers.ModelSerializer):
    ingredients_set = IngredientsSerializer(many=True, required=False)
    class Meta:
        model = MenuItems 
        fields = ('id', 'category', 'available', 'menu_item', 'unit', 'unit_price', 'ingredients_set', 'created_at', 'updated_at')

class InventoryItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryItems
        fields = ('id', 'inventory_item', 'item_category', 'quantity', 'reorder_quantity', 'unit', 'created_at', 'updated_at')

class TransactionItems(serializers.ModelSerializer):
    class Meta:
        model = TransactionItems
        fields = ('id', 'transaction', 'item')


class OrderItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItems
        fields = ('id', 'transaction', 'item', 'unit', 'unit_price', 'pcs', 'status')

class TransactionsSerializer(serializers.ModelSerializer):
    orderitems_set = OrderItemsSerializer(many=True, required=False)
    class Meta:
        model = Transactions
        fields = ('id', 'cashier_id', 'transaction_id', 'transaction_type', 'transaction_date', 
                  'table_number', 'total_amount', 'amount_given', 'discount', 'change', 'address', 'orderitems_set', 'status')


class ReservationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservations
        fields = ('id', 'date', 'time_in', 'time_out', 'name')
class TablesSerializer(serializers.ModelSerializer):
    reservations_set = ReservationsSerializer(many=True, required=False)
    class Meta:
        model = Tables
        fields = ('id', 'table_number', 'occupied', 'reservations_set', 'seats')