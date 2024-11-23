from django.db import models

# Create your models here.
class Donor(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Donor Name",
        help_text="Please provide the donor name"
    )
    email = models.EmailField(
        blank=True, 
        null=True,
        verbose_name="Donor Email (Optional)",
        help_text="Please provide the donor email"
    )
    phone = models.CharField(
        max_length=15, 
        blank=True, 
        null=True,
        verbose_name="Donor Phone (Optional)",
        help_text="Please provide the donor phone number"
    )
    address = models.TextField(
        blank=True, 
        null=True,
        verbose_name="Donor Address (Optional)",
        help_text="Please provide the donor address"
    )
    city = models.CharField(
        max_length=50, 
        blank=True,
        null=True,
        verbose_name="Donor City (Optional)",
        help_text="Please provide the donor city"
    )
    state = models.CharField(
        max_length=50, 
        blank=True, 
        null=True,
        verbose_name="Donor State (Optional)",
        help_text="Please provide the donor state"
    )
    country = models.CharField(
        max_length=50, 
        blank=True, 
        null=True,
        verbose_name="Donor Country (Optional)",
        help_text="Please provide the donor country"
    )
    zip = models.CharField(
        max_length=10, 
        blank=True, 
        null=True,
        verbose_name="Donor Zip (Optional)",
        help_text="Please provide the donor zip"
    )
    last_donated = models.DateField(
        blank=True, 
        null=True,
        verbose_name="Last Donation Date (Optional)",
        help_text="Please provide the last donation date"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-created_at']

# Donations
class Donation(models.Model):
    donor = models.ForeignKey(
        Donor, 
        on_delete=models.CASCADE,
        verbose_name="Donor associated with the donation",
        help_text="Please select the donor associated with the donation"
    )
    amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        verbose_name="Donation Amount",
        help_text="Please provide the donation amount"
    )
    date = models.DateField(
        verbose_name="Donation Date",
        help_text="Please provide the donation date"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.donor.name} - {self.amount}'

    class Meta:
        ordering = ['-created_at']

    