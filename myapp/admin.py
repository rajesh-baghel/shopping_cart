# myapp/admin.py

from django.contrib import admin
from myapp.models import Category, Item, User, CartItem, Cart

admin.site.register(Category)
admin.site.register(Item)
admin.site.register(User)
admin.site.register(CartItem)
admin.site.register(Cart)
