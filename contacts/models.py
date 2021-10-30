from django.db import models
from django.core.validators import RegexValidator

# Create your models here.
class Contact(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20, blank=True)
    phone_regex = RegexValidator(regex=r'^\+?\d{5,15}$', message="Length of number must be between 5 and 15 digits.")
    phone_number = models.CharField(validators=[phone_regex], max_length=16)
    email = models.EmailField(blank=True)
    date_born = models.DateField(blank=True)
    date_added = models.DateField(auto_now_add=True)
