from django.db import models

# Create your models here.


class Employee(models.Model):
    emp_id = models.CharField(max_length=100, primary_key=True)
    emp_name = models.CharField(max_length=200)
    emp_preferred_name = models.CharField(max_length=100, blank=True, null=True)
    emp_department = models.CharField(max_length=100)
    emp_email_id = models.CharField(max_length=200)
    emp_organization = models.CharField(max_length=100)
    std_pronunciation_audio = models.CharField(max_length=1000, blank=True, null=True)
    std_pronunciation_phonetics = models.CharField(max_length=1000, blank=True, null=True)
    custom_pronunciation_audio = models.CharField(max_length=1000, blank=True, null=True)
    custom_pronunciation_phonetics = models.CharField(max_length=1000, blank=True, null=True)