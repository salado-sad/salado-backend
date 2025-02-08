# Generated by Django 5.1.3 on 2025-02-07 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('category', models.CharField(choices=[('Vegetables', 'Vegetables'), ('Fruits', 'Fruits'), ('NutsAndSeeds', 'Nuts and Seeds'), ('ProteinsAndDairy', 'Proteins and Dairy'), ('GrainsAndCarbs', 'Grains and Carbs'), ('DressingsAndSauces', 'Dressings and Sauces'), ('Miscellaneous', 'Miscellaneous')], max_length=50)),
                ('subcategory', models.CharField(choices=[('LeafyGreens', 'Leafy Greens'), ('Cruciferous', 'Cruciferous'), ('RootVegetables', 'Root Vegetables'), ('CucumbersAndPeppers', 'Cucumbers and Peppers'), ('TomatoesAndBerries', 'Tomatoes and Berries'), ('Herbs', 'Herbs'), ('Alliums', 'Alliums'), ('Citrus', 'Citrus'), ('Tropical', 'Tropical'), ('Berries', 'Berries'), ('StoneFruits', 'Stone Fruits'), ('OtherFruits', 'Other Fruits'), ('Nuts', 'Nuts'), ('Seeds', 'Seeds'), ('Cheese', 'Cheese'), ('Meats', 'Meats'), ('PlantBased', 'Plant-Based Proteins'), ('WholeGrains', 'Whole Grains'), ('Pasta', 'Pasta'), ('BreadAndCrumbs', 'Bread and Crumbs'), ('VinegarBased', 'Vinegar-Based Dressings'), ('OilBased', 'Oil-Based Dressings'), ('Creamy', 'Creamy Dressings'), ('SpecialtySauces', 'Specialty Sauces'), ('Olives', 'Olives'), ('Pickles', 'Pickles'), ('Spices', 'Spices')], max_length=50)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('stock_quantity', models.PositiveIntegerField()),
                ('description', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='product_images/')),
            ],
        ),
    ]
