from django.db import models
from client.models import Client

# Supplies
class Supplies(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    price = models.FloatField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Supplies"
    
# SuppliesOrder
class SuppliesOrder(models.Model):
    supplies = models.ForeignKey(Supplies, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    delivery_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.supplies} - {self.client}"

    class Meta:
        verbose_name_plural = "Supply Orders"
