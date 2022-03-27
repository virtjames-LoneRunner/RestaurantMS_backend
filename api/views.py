from django.shortcuts import render
from .models import InventoryItems, MenuItems, OrderItems, Users, Categories, Transactions, TransactionItems
from .serializers import CategoriesSerializer, InventoryItemsSerializer, MenuItemsSerializer, OrderItemsSerializer, UsersSerializer, TransactionsSerializer

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response


# Create your views here.
class CategoriesView(APIView):
    serializer = CategoriesSerializer
    def get(self, request):
        all_categories = Categories.objects.all()
        return Response(CategoriesSerializer(all_categories, many=True).data, status=status.HTTP_200_OK)

    def post(self, request):
        req_data = request.data['data']
        new_category = CategoriesSerializer(data=req_data)
        if not new_category.is_valid():
            return Response({'errors': new_category.errors}, status=status.HTTP_400_BAD_REQUEST)
        new_category.save()
        return Response({'message': 'Success!'}, status=status.HTTP_201_CREATED)


class MenuItemsView(APIView):
    serializer = MenuItemsSerializer
    def get(self, request):
        all_menu_items = MenuItems.objects.filter(category=request.GET.get('category'))
        return Response(MenuItemsSerializer(all_menu_items, many=True).data, status=status.HTTP_200_OK)

    def post(self, request):
        req_data = request.data['data']
        new_menu_item = MenuItemsSerializer(data=req_data)
        if not new_menu_item.is_valid():
            return Response({'errors': new_menu_item.errors}, status=status.HTTP_400_BAD_REQUEST)
        new_menu_item.save()
        return Response({'message': 'Success!'}, status=status.HTTP_201_CREATED)

    
class InventoryItemsView(APIView):
    serializer = InventoryItemsSerializer
    def get(self, request):
        all_inventory_items = InventoryItems.objects.all()
        return Response(InventoryItemsSerializer(all_inventory_items, many=True).data, status=status.HTTP_200_OK)

    
    def post(self, request):
        req_data = request.data['data']
        new_inventory_item = InventoryItemsSerializer(data=req_data)
        if not new_inventory_item.is_valid():
            return Response({'errors': new_inventory_item.errors}, status=status.HTTP_400_BAD_REQUEST)
        new_inventory_item.save()
        return Response({'message': 'Success!'}, status=status.HTTP_201_CREATED)

class TransactionsView(APIView):
    serializer = TransactionsSerializer

    def get(self, request):
        all_transactions = Transactions.objects.all()
        
        return Response(TransactionsSerializer(all_transactions, many=True).data, status=status.HTTP_200_OK)

    def post(self, request):
        req_data = request.data['data']
        new_transaction = TransactionsSerializer(data=req_data)
        if not new_transaction.is_valid():
            return Response({'errors': new_transaction.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        # print(new_transaction)
        new_transaction.save()
        transaction = Transactions.objects.filter(transaction_id=req_data['transaction_id'])[0]
        for item in req_data['items']:
            item['transaction_id'] = transaction.id
            order_item = OrderItemsSerializer(data=item)
            print(order_item)
            if order_item.is_valid():
                order_item.save()
                order_item_added = OrderItems.objects.latest('id')
                transaction.orderitems_set.add(order_item_added)
            
            print(transaction.orderitems_set.all())
            print(order_item.errors)
            # print(item['id'])
            # transaction_item = MenuItems.objects.filter(id=item['id'])

            # print(transaction_item)
            # new_item = TransactionItems(transaction=transaction, item=transaction_item[0])
            # new_item.save()
        return Response({'message': 'Success!'}, status=status.HTTP_201_CREATED)
        