from django.db import models
from client.models import Client

# Supplies
class Supplies(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Supply Name",
        help_text="Please provide the supply name"
    )
    quantity = models.IntegerField(
        default=0,
        verbose_name="Supply Quantity",
        help_text="Please provide the supply quantity"
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name="Supply Description (Optional)",
        help_text="Please provide the supply description"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Supplies"
    
# SuppliesOrder
class SuppliesOrder(models.Model):
    supplies = models.ForeignKey(
        Supplies, 
        on_delete=models.CASCADE,
        verbose_name="Supply associated with the order",
        help_text="Please select the supply associated with the order"
    )
    quantity = models.IntegerField(
        default=1,
        verbose_name="Supply Quantity",
        help_text="Please provide the supply quantity"
    )
    client = models.ForeignKey(
        Client, 
        on_delete=models.CASCADE,
        verbose_name="Client associated with the order",
        help_text="Please select the client associated with the order"
    )
    delivery_date = models.DateField(
        verbose_name="Supply Delivery Date",
        help_text="Please provide the supply delivery date"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.supplies} - {self.client}"

    class Meta:
        verbose_name_plural = "Supply Orders"
