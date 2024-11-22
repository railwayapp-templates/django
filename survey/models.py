from django.db import models
from client.models import Client, AreaServiced

# Surveyor Profile 
class Surveyor(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    organization = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = "Survior Profile"
        verbose_name_plural = "Surviors Profiles"

# Evaluation Survey
class Survey(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=True)
    area_serviced = models.ForeignKey(AreaServiced, on_delete=models.CASCADE, null=True, blank=True)
    meet_expectations = models.BooleanField(
        choices=[(True, 'Yes'), (False, 'No')], 
        default=False,
        verbose_name="Did we meet your expectations?",
        help_text="Please select Yes or No"
    )
    volunteer_helpful = models.BooleanField(
        choices=[(True, 'Yes'), (False, 'No')], 
        default=False,
        verbose_name="Was the volunteer helpful?",
        help_text="Please select Yes or No"
    )
    comments = models.TextField(
        blank=True, 
        null=True,
        verbose_name="Additional Comments",
        help_text="Please provide any additional comments"
    )
    service_impact = models.TextField(
        blank=True, 
        null=True,
        verbose_name="How did the service impact you?",
        help_text="Please provide any additional comments"
    )
    refer_friends = models.BooleanField(
        choices=[(True, 'Yes'), (False, 'No')], 
        default=False,
        verbose_name="Would you refer your friends to our service?",
        help_text="Please select Yes or No"
    )
    date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"Survey {self.id}"
    
    class Meta:
        verbose_name = "Evaluation Survey"
        verbose_name_plural = "Evaluation Surveys"

# 2024 Client Survey
class ClientSurvey2024(models.Model):
    survior = models.ForeignKey(Surveyor, on_delete=models.CASCADE, null=True, blank=True)
    area_serviced = models.ForeignKey(AreaServiced, on_delete=models.CASCADE, null=True, blank=True)
    uti_lastyear = models.BooleanField(
        choices=[(True, 'Yes'), (False, 'No')], 
        default=False,
        verbose_name="Have you had a Urinary Tract Infection (UTI) in the last year?",
        help_text="Please select Yes or No"
    )
    medical_treatment = models.CharField(
        max_length=20,
        choices=[
            ('Doctor', 'Doctor'),
            ('ER', 'ER'),
            ('Urgent Care', 'Urgent Care'),
            ('N/A', 'N/A')
        ],
        default='N/A',
        verbose_name="If you sought medical care, did you have to see a doctor or go to the ER?",
        help_text="Please select the appropriate option"
    )
    distance_to_healthcare = models.CharField(
        max_length=50,
        choices=[
            ('Within a mile', 'Within a mile'),
            ('Further than a mile but within five miles', 'Further than a mile but within five miles'),
            ('Further than five miles', 'Further than five miles')
        ],
        default='Within a mile',
        verbose_name="How far away from health care do you live?",
        help_text="Please select the appropriate option"
    )
    used_leakage_items = models.BooleanField(
        choices=[(True, 'Yes'), (False, 'No')],
        default=False,
        verbose_name="Have you ever used items to assist with leakage other than adult diapers, bladder pads/products (such as towels, sheets, washcloths etc.)?",
        help_text="Please select Yes or No"
    )
    helped_leave_home = models.CharField(
        max_length=50,
        choices=[
            ('Doctors appointments', 'Go to doctors appointments'),
            ('Shop', 'Shop'),
            ('Attend church', 'Attend church'),
            ('Socialize', 'Socialize'),
            ('Other', 'Other')
        ],
        default='Doctors appointments',
        verbose_name="Has having incontinent products helped you to leave home more to:",
        help_text="Please select the appropriate option"
    )

    class Meta:
        verbose_name = "2024 Client Survey"
        verbose_name_plural = "2024 Client Surveys"