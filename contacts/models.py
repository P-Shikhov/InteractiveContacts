from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django import forms
from django.utils import timezone
import datetime

# from email_and_uname_auth.models import CustomUser
from contact_book import settings

def validate_date_born(date_born):
    if date_born > datetime.date.today(): 
        raise ValidationError("Date of birth must precede the current date.")

class Contact(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20, blank=True)
    phone_regex = RegexValidator(regex=r'^\+?\d{3,15}$', message="Phone number must include 5 to 15 digits.")
    phone_number = models.CharField(validators=[phone_regex], max_length=16)
    email = models.EmailField(blank=True)
    date_born = models.DateField(blank=True, validators=[validate_date_born])
    date_added = models.DateField(auto_now_add=True)


class LogEntry(models.Model):
    class ActionType(models.TextChoices):
        CALL = 'Call'
        EMAIL = 'Email'
        IM = 'IM'

    class Result(models.TextChoices):
        SUCCESS = 'Success'
        FAILURE = 'Failure'

    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now())
    action = models.CharField(
        choices=ActionType.choices, 
        max_length=5, 
        default=ActionType.CALL
    )
    result = models.CharField(
        choices=Result.choices, 
        max_length=7, 
        default=Result.SUCCESS
    )
    comment = models.TextField(max_length=150, blank=True)
