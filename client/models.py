from django.db import models

# Ethnicity choices


class Ethnicity(models.TextChoices):
    ASIAN = 'AS', 'Asian'
    BLACK = 'BL', 'Black'
    HISPANIC = 'HI', 'Hispanic'
    WHITE = 'WH', 'White'
    OTHER = 'OT', 'Other'

# Client model


class Client(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    zip = models.CharField(max_length=10)
    country = models.CharField(max_length=200)
    ethnicity = models.CharField(
        max_length=2,
        choices=Ethnicity.choices,
        default=Ethnicity.OTHER,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
