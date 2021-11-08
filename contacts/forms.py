from django import forms

from .models import Contact, LogEntry

class DateInput(forms.DateInput):
    input_type = 'date'

class ContactCreationForm(forms.ModelForm):

    class Meta:
        model = Contact
        fields = (
            'first_name', 
            'last_name',
            'phone_number',
            'email',
            'date_born',
        )
        widgets = {
            'date_born': DateInput(),
        }


# class CustomUserChangeForm(UserChangeForm):

#     class Meta:
#         model = CustomUser
#         fields = ('email',)


class LogEntryCreationForm(forms.ModelForm):

    class Meta:
        model = LogEntry
        fields = (
            'date', 
            'action',
            'result',
            'comment',
        )
        widgets = {
            'result': forms.RadioSelect
        }
