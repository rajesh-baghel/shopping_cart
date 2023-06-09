# myapp/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Category, Item, CartItem, Cart, User
from .serializers import CategorySerializer, ItemSerializer, CartItemSerializer, CartSerializer, UserSerializer


class CategoryListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


class ItemListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)


class ItemFilterView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, category_id):
        items = Item.objects.filter(category=category_id)
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)


class CartView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        user = request.user

        if user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=user)
            serializer = CartSerializer(cart)
            return Response(serializer.data)
        else:
            return Response({'detail': 'Cart is empty.'})

class CartItemView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        user = request.user
        cart = None

        if user.is_authenticated:
            # Authenticated user
            cart, created = Cart.objects.get_or_create(user=user)
        else:
            # Guest user
            cart, created = Cart.objects.get_or_create(user=None)

        item_id = request.data.get('item_id')
        quantity = request.data.get('quantity', 1)

        # Retrieve the item
        item = Item.objects.get(pk=item_id)

        # Calculate the price
        price = item.price * int(quantity)

        # Check if the item is already in the cart
        cart_item, created = CartItem.objects.get_or_create(cart=cart, item=item)

        if not created:
            # Item already exists in the cart, update the quantity and price
            cart_item.quantity += int(quantity)
            cart_item.price = item.price * cart_item.quantity
            cart_item.save()
        else:
            # Create a new cart item
            cart_item.quantity = quantity
            cart_item.price = price
            cart_item.save()

        # Update the cart's total price
        cart.update_total_price()
        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data)



class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = User.objects.filter(email=email).first()

        if user is None or not user.check_password(password):
            return Response({'error': 'Invalid email or password'}, status=400)

        refresh = RefreshToken.for_user(user)
        serializer = UserSerializer(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': serializer.data
        })
