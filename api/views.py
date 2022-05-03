from doctest import master
from re import M
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

class UsersView(APIView):
    def get(self, request):
        users = User.objects.all()
        users_ = []

        for user in users:
            role = "Non-Admin"
            if user.is_superuser:
                role = 'Admin'
            users_.append({'id': user.id, 'role': role , 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email, 'last_login': user.last_login})
        

        return Response({'users' : users_}, status=200)

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
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
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
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
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
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer = TransactionsSerializer

    def get(self, request):
        all_transactions = Transactions.objects.order_by('-id').all()
        
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
            print(item)
            order_item = OrderItemsSerializer(data=item)
            menu_item = MenuItems.objects.get(id=item['id'])
            ingredients = menu_item.ingredients_set.all()
            for ingredient in ingredients:
                edit_inventory = InventoryItems.objects.get(id=ingredient.item_id)
                print("Ingredient Quantity", ingredient.quantity)
                print('Edit Inventory', edit_inventory.quantity)
                edit_inventory.quantity = edit_inventory.quantity - (ingredient.quantity * float(item['pcs']))
                edit_inventory.save()
            if order_item.is_valid():
                order_item.save()
                order_item_added = OrderItems.objects.order_by('-id')[0]

                
                transaction.orderitems_set.add(order_item_added)
            else:
                print(order_item.errors)
            
            print(transaction.orderitems_set.all())
            
        return Response({'message': 'Success!'}, status=status.HTTP_201_CREATED)


class OrdersView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer = TransactionsSerializer
    

    def get(self, request):
        state = request.GET.get('state')
        transactions = Transactions.objects.filter(status=state).all()
            
        transactions_orders = []

        for transaction in transactions:
            orders = []
            for order in transaction.orderitems_set.all():
                orders.append(OrderItemsSerializer(order).data)

            if not orders:
                continue
            transactions_orders.append({"id": transaction.id,
                                        "transaction_id": transaction.transaction_id, "transaction_type": transaction.transaction_type, 
                                        "transaction_date": transaction.transaction_date, "table_number": transaction.table_number,
                                        "status": transaction.status,
                                        "orderitems_set": orders})

        if state == "Not Started":
            transactions_ = Transactions.objects.filter(status="Started").all()
            for transaction in transactions_:
                orders = []
                for order in transaction.orderitems_set.all():
                    orders.append(OrderItemsSerializer(order).data)

                if not orders:
                    continue
                transactions_orders.append({"id": transaction.id,
                                            "transaction_id": transaction.transaction_id, "transaction_type": transaction.transaction_type, 
                                            "transaction_date": transaction.transaction_date, "table_number": transaction.table_number,
                                            "status": transaction.status,
                                            "orderitems_set": orders})
            
        return Response(transactions_orders, status=200)

    
    def patch(self, request):
        print(request.data)
        try:
            transaction = Transactions.objects.filter(id=int(request.data['data']['transaction_id'])).first()
            masterStatus = request.data['data']['masterStatus']
            if masterStatus == "Done" and transaction.status == "Done":
                masterStatus = "Started"
            elif masterStatus == "Not Done":
                masterStatus = "Done"
            elif masterStatus == "Not Started":
                masterStatus = "Not Started"
                for order in transaction.orderitems_set.all():
                    order.status = "Not Started"

            transaction.status = masterStatus
            transaction.save()
        except KeyError as e:
            print(e)
            orderItem = OrderItems.objects.filter(id=int(request.data['data']['order_id'])).first()
            transaction = Transactions.objects.filter(id=orderItem.transaction.id).first()

            orderItem.status = request.data['data']['order_status']

            if orderItem.status == "Done" or orderItem.status == "Started":
                transaction.status = "Started"
            else:
                transaction.status = "Not Started"


            orderItem.save()
            transaction.save()

        return Response({"message": "Done"}, status=200)


