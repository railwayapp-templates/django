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
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        verbose_name="Client associated with the order",
        help_text="Please select the client associated with the order"
    )
    supplies = models.ForeignKey(
        Supplies, 
        on_delete=models.CASCADE,
        verbose_name="Supply associated with the order",
        help_text="Please select the supply associated with the order"
    )
    supplies_other = models.CharField(
        max_length=256,
        null=True,
        blank=True,
        verbose_name="Other supplies not listed above",
        help_text="Please provide the supply name if not listed above"
    )
    quantity = models.IntegerField(
        default=1,
        verbose_name="Supply Quantity",
        help_text="Please provide the supply quantity"
    )
    delivery_date = models.DateField(
        verbose_name="Supply Recieved Date",
        help_text="Please provide the supply delivery date in the following format with dashes (year-month-date) or use the date selected on the right."
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.supplies} - {self.client}"

    class Meta:
        verbose_name_plural = "Supply Orders"
