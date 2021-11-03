from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator


class CustomUserManager(BaseUserManager):
    def create_user(self, first_name, last_name, email, username, password, **other_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(
            email=email, 
            username=username.lower(), 
            first_name=first_name, 
            last_name=last_name, 
            **other_fields)
        user.set_password(password)
        user.save()
        return user

    

    def create_superuser(self, email, username, password, **other_fields):
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_superuser') is False:
            raise ValueError('Superuser must have is_superuser set to True')
        if other_fields.get('is_staff') is False:
            raise ValueError('Superuser must have is_staff set to True')
        if other_fields.get('is_active') is False:
            raise ValueError('Superuser must have is_active set to True')
        return self.create_user(
            email=self.normalize_email(email), 
            username=username, 
            password=password, 
            **other_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=20, blank=False)
    last_name = models.CharField(max_length=20, blank=False)
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(_('username'), max_length=30, unique=True,
        help_text=_('Required. 30 characters or fewer. Letters, digits and '
                    '@/./+/-/_ only.'),
        validators=[
            RegexValidator(r'^[\w-]{5,30}$',
                                      _('Enter a valid username. '
                                        'This value may contain only letters, numbers '
                                        'and dash.'), 'invalid'),
        ],
        error_messages={
            'unique': _("A user with that username already exists."),
        })
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']


