# Generated by Django 5.1.3 on 2025-03-07 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0004_package_stock_quantity_alter_package_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='package',
            name='products',
            field=models.JSONField(default=list, null=True),
        ),
    ]
