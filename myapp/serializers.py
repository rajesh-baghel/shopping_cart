# serializers.py

from rest_framework import serializers
from .models import Category, Item, CartItem, Cart, User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'


class CartItemSerializer(serializers.ModelSerializer):
    item = ItemSerializer()

    class Meta:
        model = CartItem
        fields = ['id', 'item', 'quantity', 'price']


class CartSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'total_price', 'cart_items']
        read_only_fields = ['user', 'total_price']

    def create(self, validated_data):
        cart_items_data = self.context.get('request').data.get('cart_items')
        cart = Cart.objects.create(user=self.context.get('request').user)

        for item_data in cart_items_data:
            item = Item.objects.get(pk=item_data['item'])
            quantity = item_data['quantity']
            price = item.price * quantity
            CartItem.objects.create(cart=cart, item=item, quantity=quantity, price=price)

        return cart


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'address', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone_number=validated_data['phone_number'],
            address=validated_data['address'],
            password=validated_data['password']
        )
        return user
