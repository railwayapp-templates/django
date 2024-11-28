# forms.py

from django import forms
from django.forms import inlineformset_factory
from .models import SuppliesOrder, OrderItem
from unfold.widgets import UnfoldAdminDateWidget, UnfoldAdminSplitDateTimeWidget

class SuppliesOrderForm(forms.ModelForm):
    class Meta:
        model = SuppliesOrder
        fields = '__all__'

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = '__all__'

OrderItemFormSet = inlineformset_factory(
    SuppliesOrder, 
    OrderItem, 
    form=OrderItemForm, 
    extra=1, 
    can_delete=True
)