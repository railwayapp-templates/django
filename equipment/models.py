from django.db import models
from client.models import Client

# Create your models here.
class Equipment(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    stock = models.IntegerField()
    image = models.ImageField(upload_to="equipment/images")
    barcode = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
class Order(models.Model):
    class Status(models.TextChoices):
        RENTED = 'RT', 'Rented'
        RETURNED = 'RU', 'Returned'

    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    last_updated = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.RENTED,
    )

    def __str__(self):
        return f"{self.equipment} - {self.client}"
