from django.apps import AppConfig

from django.apps import AppConfig
from django.db.models.signals import post_migrate

def create_groups(sender, **kwargs):
    from django.contrib.auth.models import Group
    GROUPS = ['vendor', 'customer', 'saladoadmin', 'delivery']
    for group_name in GROUPS:
        Group.objects.get_or_create(name=group_name)

class AuthSystemConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'auth_system'
    
    def ready(self):
        post_migrate.connect(create_groups, sender=self)
