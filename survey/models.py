from django.db import models

# Client Survey
class Survey(models.Model):
    meet_expectations = models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False)
    volunteer_helpful = models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False)
    comments = models.TextField(blank=True, null=True)
    service_impact = models.TextField()
    refer_friends = models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False)
    date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"Survey {self.id}"