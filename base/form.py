from .models import Product
from django.forms import ModelForm
from django.contrib.auth.models import User


class Product_creation_form(ModelForm):
    class Meta:
        model=Product
        fields=['name', 'description', 'image', 'price', 'category']


