# Generated by Django 5.1.3 on 2025-02-08 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0002_remove_package_products'),
    ]

    operations = [
        migrations.AddField(
            model_name='package',
            name='products',
            field=models.JSONField(default=list),
        ),
        migrations.DeleteModel(
            name='PackageProduct',
        ),
    ]
