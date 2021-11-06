from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
import datetime

# from email_and_uname_auth.models import CustomUser
from contact_book import settings
from .middleware import get_request

def validate_date_born(date_born):
    if date_born > datetime.date.today(): 
        raise ValidationError("Date of birth must precede the current date.")

class Contact(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20, blank=True)
    phone_regex = RegexValidator(regex=r'^\+?\d{5,15}$', message="Phone number must include 5 to 15 digits.")
    phone_number = models.CharField(validators=[phone_regex], max_length=16)
    email = models.EmailField(blank=True)
    date_born = models.DateField(blank=True, validators=[validate_date_born])
    date_added = models.DateField(auto_now_add=True)

    # def save(self):
    #     request = get_request()
    #     # if request.user == self.user or request.user.is_superuser:
    #     if request.user == self.user:
    #         self.user = request.user
    #         super().save()
    #     else:
    #         return
