from django.utils import timezone
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


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

    order_status = models.CharField(max_length=25, choices=ORDER_STATUSES, default=ORDER_STATUSES[0][0])
    customer = models.ForeignKey(User)
    delivery_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    address = models.CharField(max_length=100)

    def __str__(self):
        return f"<Order to be delivered for {self.customer} to {self.address}>"

class OrderItem(models.Model):
    item = models.ForeignKey(MenuItem)
    order = models.ForeignKey(Order)
    quantity = models.IntegerField(default=1)

    @property
    def subtotal(self):
        return "%.2f" % (float(self.item.price) * int(self.quantity))