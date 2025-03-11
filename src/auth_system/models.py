from django.contrib.auth.models import AbstractUser
from django.db import models

class SaladoUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=False, unique=True, verbose_name="Phone Number")
    first_name = models.CharField(max_length=30, blank=True, null=False, verbose_name="First Name")
    last_name = models.CharField(max_length=30, blank=True, null=False, verbose_name="Last Name")
    date_of_birth = models.DateField(blank=True, null=True, verbose_name="Date of Birth")
    national_code = models.CharField(max_length=10, blank=True, null=False, unique=True, verbose_name="National Code")
    address = models.TextField(blank=True, null=True, verbose_name="Address")  # New field
    company = models.CharField(max_length=100, blank=True, null=True, verbose_name="Company")  # New field

    REQUIRED_FIELDS = ['email', 'phone_number', 'first_name', 'last_name', 'date_of_birth', 'national_code']

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='saladouser_set',  # Change the reverse relation name
        blank=True
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='saladouser_permissions',  # Change the reverse relation name
        blank=True
    )

    def __str__(self):
        return self.username
