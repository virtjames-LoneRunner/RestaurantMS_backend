from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


from .models import Ingredients, InventoryItems, MenuItems, OrderItems, Categories, Transactions, TransactionItems
from .serializers import CategoriesSerializer, InventoryItemsSerializer, MenuItemsSerializer, OrderItemsSerializer, TransactionsSerializer

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class Authentication(APIView):
    def get(self, request):
        pass
    def post(self, request):
        req_data = request.data
        # try:
        #     user = User.objects.get(username=req_data['username'])
        # except User.DoesNotExist:
        #     return Response({"errors": {'username': ['User does not exist']}}, status=400)
        
        user = authenticate(username=req_data['username'], password=req_data['password'])
        if not user:
            return Response({'errors': {'password': ['Invalid password']}}, status=401)

        token, created = Token.objects.get_or_create(user=user)
        print(token)
        print(user.is_staff)

        return Response({'user_id': user.id, 'user_email': user.email, 'token': str(token), 'auth': user.is_staff}, status=status.HTTP_200_OK)





class CategoriesView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
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
        all_menu_items = MenuItems.objects.filter(category=request.GET.get('category')).all()
        for menu_item in all_menu_items:
            available = True
            ingredients_set = menu_item.ingredients_set.all()
            if not ingredients_set:
                continue
            for item in ingredients_set:
                inventory = InventoryItems.objects.get(id=item.item_id)
                if inventory.quantity >= item.quantity:
                    available = True
                else:
                    available = False
            menu_item.available = available
            menu_item.save()

        return Response(MenuItemsSerializer(all_menu_items, many=True).data, status=status.HTTP_200_OK)

    def post(self, request):
        req_data = request.data['data']
        category = Categories.objects.get(id=int(req_data['category']))
        new_item = MenuItems.objects.create(category=category, available=req_data['available'], 
                                            menu_item=req_data['menu_item'], unit=req_data['unit'], unit_price=req_data['unit_price'])
        
        new_item.save()
        new_item = MenuItems.objects.latest('id')

        for ingredient in req_data['ingredient_set']:
            new_ingredient = Ingredients.objects.create(menu_item=new_item, item_id=ingredient['item']['id'], item=ingredient['item']['item'], unit=ingredient['unit'], quantity=ingredient['quantity'])
            new_ingredient.save()
            # ingredient_added = Ingredients.objects.latest('id')
            # new_item.ingredient_set.add(new_ingredient)

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
            
        return Response({'message': 'Success!'}, status=status.HTTP_201_CREATED)
        