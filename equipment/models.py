from django.db import models
from client.models import Client

# Create your models here.
class Equipment(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Equipment Name",
        help_text="Please provide the equipment name"
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name="Equipment Description (Optional)",
        help_text="Please provide the equipment description"
    )
    stock = models.IntegerField(
        default=0,
        verbose_name="Equipment Stock",
        help_text="Please provide the equipment stock count"
    )
    barcode = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Equipment Barcode or Serial Number (Optional)",
        help_text="Please provide the equipment barcode or serial number"
    )
    def __str__(self):
        return self.name
    
class DMEOrder(models.Model):
    class Status(models.TextChoices):
        RENTED = 'RT', 'Rented'
        RETURNED = 'RU', 'Returned'
    
    client = models.ForeignKey(
        Client, 
        on_delete=models.CASCADE,
        verbose_name="Client associated with the order",
        help_text="Please select the client associated with the order"
    )
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.RENTED,
        verbose_name="Order Status",
        help_text="Please select the order status"
    )
    rental_date = models.DateField(
        verbose_name="Rental Date",
        help_text="Please provide date the equipment was rented"
    )
    last_updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.client.name} - {self.rental_date}"
    
    class Meta:
        verbose_name_plural = "Durables Medical Equipment Orders"
        verbose_name = "Durables Medical Equipment Order"

class DMEOrderItem(models.Model):
    order = models.ForeignKey(
        DMEOrder, 
        related_name='items',
        on_delete=models.CASCADE
    )
    equipment = models.ForeignKey(
        Equipment, 
        on_delete=models.CASCADE,
        verbose_name="Equipment associated with the order",
        help_text="Please select the equipment associated with the order"
    )
    quantity = models.IntegerField(
        default=0,
        verbose_name="Equipment Quantity",
        help_text="Please provide the equipment quantity"
    )
    last_updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.equipment} - {self.quantity}"
