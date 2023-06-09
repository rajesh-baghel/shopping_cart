from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=255)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name





class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    total_price = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def update_total_price(self):
        self.total_price = self.cartitem_set.aggregate(models.Sum('price'))['price__sum'] or 0
        self.save()

    def __str__(self):
        if self.user:
            return f"{self.user.username}'s Cart"
        else:
            return "Guest Cart"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def subtotal(self):
        return self.quantity * self.item.price

    def __str__(self):
        return f"CartItem {self.item} in {self.cart}"


