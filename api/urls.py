from django.urls import path

from .views import CategoriesView, InventoryItemsView, MenuItemsView, TransactionsView, Authentication, UsersView

urlpatterns = [
    path('users/', UsersView.as_view()),
    path('auth/', Authentication.as_view()),
    path('categories/', CategoriesView.as_view()),
    path('menu-items/', MenuItemsView.as_view()),
    path('inventory-items/', InventoryItemsView.as_view()),
    path('transactions/', TransactionsView.as_view())
]
