from django import forms
from unfold.widgets import UnfoldAdminRadioSelectWidget, UnfoldAdminCheckboxSelectMultiple
from .models import ClientSurvey2024

class ClientSurvey2024Form(forms.ModelForm):
    medical_treatment = forms.MultipleChoiceField(
        choices=[
            ('Doctor', 'Doctor'),
            ('ER', 'ER'),
            ('Urgent Care', 'Urgent Care'),
            ('N/A', 'N/A')
        ],
        widget=UnfoldAdminCheckboxSelectMultiple,
        required=False
    )

    helped_leave_home = forms.MultipleChoiceField(
        choices=[
            ("Doctors", "Go to doctor's appointments"),
            ("Shop", "Shop"),
            ("Attend church", "Attend church"),
            ("Socialize", "Socialize")
        ],
        widget=UnfoldAdminCheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = ClientSurvey2024
        fields = '__all__'
        widgets = {
            'uti_lastyear': UnfoldAdminRadioSelectWidget(),
            'distance_to_healthcare': UnfoldAdminRadioSelectWidget(),
            'used_leakage_items': UnfoldAdminRadioSelectWidget(),
        }

    def clean_medical_treatment(self):
        return self.cleaned_data.get('medical_treatment', [])