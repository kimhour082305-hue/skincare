from django.db.models import Count
from .models import Category

def category_context(request):
    return {
        'nav_categories': Category.objects.annotate(product_count=Count('products'))
    }
