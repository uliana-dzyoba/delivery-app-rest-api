from django.utils import timezone
from django.db import models
from django.conf import settings


# Create your models here.
class MenuItem(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Order(models.Model):
    ORDER_STATUSES = (
        ('PENDING', 'Pending'),
        ('IN_TRANSIT', 'In transit'),
        ('DELIVERED', 'Delivered')
    )

    order_status = models.CharField(max_length=25, choices=ORDER_STATUSES, default='PENDING')
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    delivery_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    address = models.CharField(max_length=100)

    def __str__(self):
        return f"<Order to be delivered for {self.user} to {self.address}>"

class OrderItem(models.Model):
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    quantity = models.IntegerField(default=1)
