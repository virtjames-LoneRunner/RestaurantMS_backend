from django.urls import path

from api.views import CategoriesView, InventoryItemsView, MenuItemsView

urlpatterns = [
    path('categories/', CategoriesView.as_view()),
    path('menu-items/', MenuItemsView.as_view()),
    path('inventory-items/', InventoryItemsView.as_view())
]
