# myapp/models.py

from django.db import models

class HealthInsurance(models.Model):
    plan_name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.plan_name
