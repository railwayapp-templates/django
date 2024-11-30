# forms.py

from django import forms
from django.forms import inlineformset_factory

from unfold.widgets import UnfoldAdminRadioSelectWidget

from .models import DMEOrder, DMEOrderItem

class DMEOrderForm(forms.ModelForm):
    status = forms.ChoiceField(
        choices=[
            ('RT', 'Rented'),
            ('RU', 'Returned')
        ],
        widget=UnfoldAdminRadioSelectWidget()
    )
    class Meta:
        model = DMEOrder
        fields = '__all__'

class DMEOrderItemForm(forms.ModelForm):
    class Meta:
        model = DMEOrderItem
        fields = '__all__'

DMEOrderItemFormSet = inlineformset_factory(
    DMEOrder, 
    DMEOrderItem, 
    form=DMEOrderItemForm, 
    extra=1, 
    can_delete=True
)