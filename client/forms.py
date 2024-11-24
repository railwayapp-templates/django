# forms.py
from django import forms
from unfold.widgets import UnfoldAdminRadioSelectWidget, UnfoldAdminSelectWidget
from .models import Client

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'
        widgets = {
            'gender': UnfoldAdminRadioSelectWidget(),
            'ethnicity': UnfoldAdminRadioSelectWidget(),
        }