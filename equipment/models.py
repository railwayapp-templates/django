from django.db import models

# Create your models here.
class Equipment(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    stock = models.IntegerField()
    image = models.ImageField(upload_to="equipment/images")
    barcode = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
