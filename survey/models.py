from django.db import models
from django import forms
from client.models import Client, AreaServiced

# Surveyor Profile 
class Surveyor(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    organization = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        verbose_name = "Surveyor Profile"
        verbose_name_plural = "Surveyors Profiles"

# Evaluation Survey
class Survey(models.Model):
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
    zipcode = models.CharField(
        max_length=10, 
        null=True, 
        blank=True,
        verbose_name="Zipcode",
        help_text="Please provide your zipcode"
    )

    date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"Survey {self.id}"
    
    class Meta:
        verbose_name = "Evaluation Survey"
        verbose_name_plural = "Evaluation Surveys"


# Zipcode Survey
class ZipcodeSurvey(models.Model):
    zipcode = models.CharField(
        max_length=10, 
        null=True, 
        blank=True,
        verbose_name="Zipcode",
        help_text="Please provide your zipcode"
    )

    def __str__(self):
        return f"{self.zipcode}"
    
# 2024 Client Survey
class ClientSurvey2024(models.Model):
    uti_lastyear = models.BooleanField(
        choices=[(True, 'Yes'), (False, 'No')], 
        verbose_name="Have you had a Urinary Tract Infection (UTI) in the last year?",
        help_text="Please select Yes or No"
    )

    medical_treatment = models.JSONField(
        default=list,
        verbose_name="If you sought medical care, did you have to see a doctor or go to the ER?",
        help_text="Please select the appropriate options"
    )

    distance_to_healthcare = models.CharField(
        max_length=50,
        choices=[
            ('Within a mile', 'Within a mile'),
            ('Further than a mile but within five miles', 'Further than a mile but within five miles'),
            ('Further than five miles', 'Further than five miles')
        ],
        verbose_name="How far away from health care do you live?",
        help_text="Please select the appropriate option"
    )

    used_leakage_items = models.BooleanField(
        choices=[(True, 'Yes'), (False, 'No')],
        verbose_name="Have you ever used items to assist with leakage other than adult diapers, bladder pads/products (such as towels, sheets, washcloths etc.)?",
        help_text="Please select Yes or No"
    )

    helped_leave_home = models.JSONField(
        default=list,
        verbose_name="Has having incontinent products helped you to leave home more to:",
        help_text="Please select the appropriate options"
    )

    other_comments = models.TextField(
        blank=True, 
        null=True,
        verbose_name="Additional Comments (Other)",
        help_text="Please provide any additional comments"
    )

    zipcode = models.ForeignKey(
        ZipcodeSurvey, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        verbose_name="Zipcode",
        help_text="Please provide your zipcode"
    )
    surveyor = models.ForeignKey(
        Surveyor, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        verbose_name="Surveyor",
        help_text="Please select the surveyor"
    )
    date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Date of Survey",
        help_text="Please provide the date of the survey"
    )

    class Meta:
        verbose_name = "2024 Client Survey"
        verbose_name_plural = "2024 Client Surveys"
    
    def __str__(self):
        return f"{self.zipcode} - {self.surveyor}"