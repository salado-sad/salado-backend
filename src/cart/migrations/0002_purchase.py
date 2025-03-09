# Generated by Django 5.1.3 on 2025-03-09 21:54

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0001_initial'),
        ('management', '0009_package_is_active'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('status', models.CharField(default='Awaiting admin approval', max_length=50)),
                ('purchased_at', models.DateTimeField(auto_now_add=True)),
                ('package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management.package')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchases', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
