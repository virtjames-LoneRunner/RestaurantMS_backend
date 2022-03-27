from django.contrib import admin

from api.models import Categories
from api.models import MenuItems
from api.models import InventoryItems


# Register your models here.
admin.site.register(Categories)
admin.site.register(MenuItems)
admin.site.register(InventoryItems)