from django.urls import path
from myapp.views import (
    CategoryListView,
    ItemListView,
    ItemFilterView,
    CartView,
    CartItemView,
    UserLoginView,
)

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('items/', ItemListView.as_view(), name='item-list'),
    path('items/<int:category_id>/', ItemFilterView.as_view(), name='item-filter'),
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/items/', CartItemView.as_view(), name='cart-item'),
    path('login/', UserLoginView.as_view(), name='login'),
]
