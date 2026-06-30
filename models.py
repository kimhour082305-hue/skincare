from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200)
    brand = models.CharField(max_length=100)
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    discount_percentage = models.IntegerField(default=0)
    image = models.ImageField(upload_to='products/')
    stock = models.IntegerField(default=10)
    
    # Custom items for the Rothrr Detail Panel view
    weight = models.CharField(max_length=50, default="150g (0.33 lbs)")
    spf = models.CharField(max_length=50, default="SPF50+ PA++++")
    product_type = models.CharField(max_length=100, default="Very High Protection")

    def __str__(self):
        return self.name