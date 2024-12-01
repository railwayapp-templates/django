# forms.py
from django import forms

from .models import Donor

class DonorForm(forms.ModelForm):
    class Meta:
        model = Donor
        fields = '__all__'
