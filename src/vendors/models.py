from django.db import models
from auth_system.models import SaladoUser

class Product(models.Model):
    CATEGORY_CHOICES = [
        ("Vegetables", "Vegetables"),
        ("Fruits", "Fruits"),
        ("Grains", "Grains"),
        ("Proteins", "Proteins"),
        ("Dairy", "Dairy"),
        ("HerbsAndSpices", "Herbs and Spices"),
        ("OilsAndVinegars", "Oils and Vinegars"),
        ("NutsAndSeeds", "Nuts and Seeds"),
        ("Condiments", "Condiments"),
    ]

    SUBCATEGORY_CHOICES = [

        ("LeafyGreens", "Leafy Greens"),
        ("Cruciferous", "Cruciferous"),
        ("Root", "Root Vegetables"),
        ("Allium", "Alliums"),
        ("Nightshades", "Nightshades"),
        ("Legumes", "Legumes"),
        ("Mushrooms", "Mushrooms"),
        ("Squashes", "Squashes"),


        ("Citrus", "Citrus"),
        ("Tropical", "Tropical Fruits"),
        ("Berries", "Berries"),
        ("StoneFruits", "Stone Fruits"),
        ("Pomes", "Pome Fruits"),
        ("Melons", "Melons"),


        ("WholeGrains", "Whole Grains"),
        ("Pasta", "Pasta"),
        ("Breads", "Breads"),


        ("Meat", "Meat"),
        ("Seafood", "Seafood"),
        ("PlantBased", "Plant-Based Proteins"),


        ("Milk", "Milk"),
        ("Cheese", "Cheese"),
        ("Yogurt", "Yogurt"),


        ("Herbs", "Herbs"),
        ("Spices", "Spices"),


        ("Oils", "Oils"),
        ("Vinegars", "Vinegars"),


        ("Nuts", "Nuts"),
        ("Seeds", "Seeds"),


        ("Sauces", "Sauces"),
        ("Pastes", "Pastes"),
    ]

    MEASUREMENT_UNITS = [
        ("grams", "Grams"),
        ("kilograms", "Kilograms"),
        ("milliliters", "Milliliters"),
        ("liters", "Liters"),
        ("pieces", "Pieces"),
    ]

    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(SaladoUser, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    subcategory = models.CharField(max_length=50, choices=SUBCATEGORY_CHOICES)
    catalogue_name = models.CharField(max_length=255, blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    stock_quantity = models.PositiveIntegerField()
    product_measurement = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    measurement_unit = models.CharField(max_length=20, choices=MEASUREMENT_UNITS, default="grams")
    image = models.ImageField(upload_to="product_images/", blank=True, null=True)

    def __str__(self):
        return self.name
