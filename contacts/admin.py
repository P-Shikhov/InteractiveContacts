from django.contrib import admin
from django.db import models
from django.contrib import admin

from .models import Contact

class ContactAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'phone_number', 'id')
    readonly_fields = (id,)

admin.site.register(Contact, ContactAdmin)
