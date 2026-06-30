from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'category', 'name', 'brand', 'code', 'description', 
            'price', 'original_price', 'discount_percentage', 
            'image', 'stock', 'weight', 'spf', 'product_type'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Apply structured inline styles to form input layouts automatically
        for field_name, field in self.fields.items():
            if field_name not in ['description', 'category', 'image']:
                field.widget.attrs.update({
                    'style': 'width: 100%; padding: 10px; border: 1px solid #ccc; border-radius: 4px; margin-bottom: 15px; box-sizing: border-box;'
                })
            elif field_name == 'description':
                field.widget.attrs.update({
                    'rows': 4,
                    'style': 'width: 100%; padding: 10px; border: 1px solid #ccc; border-radius: 4px; margin-bottom: 15px; box-sizing: border-box; resize: vertical;'
                })
            elif field_name == 'category':
                field.widget.attrs.update({
                    'style': 'width: 100%; padding: 10px; border: 1px solid #ccc; border-radius: 4px; margin-bottom: 15px; box-sizing: border-box; background-color: #fff;'
                })