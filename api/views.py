from django.shortcuts import render
from .models import InventoryItems, MenuItems, Users, Categories
from .serializers import CategoriesSerializer, InventoryItemsSerializer, MenuItemsSerializer, UsersSerializer

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
