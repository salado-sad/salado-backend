from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class SaladoUser(AbstractUser):
    first_name = models.CharField(max_length=30, blank=True, null=False, verbose_name="First Name")
    last_name = models.CharField(max_length=30, blank=True, null=False, verbose_name="Last Name")
    date_of_birth = models.DateField(blank=True, null=True, verbose_name="Date of Birth")
    phone_number = models.CharField(max_length=15, blank=True, null=False, unique=True, verbose_name="Phone Number")
    national_code = models.CharField(max_length=10, blank=True, null=False, unique=True, verbose_name="National Code")

    # TODO: Why I added this?
    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_set',
        blank=True,
    )

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.email} {self.password}"
