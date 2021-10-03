from django import forms
from .models import *

class AddProductForm(forms.ModelForm):
    class Meta :
        model = Product
        fields = '__all__'


class AddCatalogForm(forms.ModelForm):
    class Meta :
        model = Catalogue
        fields = ['title', 'description', 'image']

class AddBrandForm(forms.ModelForm):
    class Meta :
        model = Brand
        fields = ['name', 'image']

class OrderForm(forms.ModelForm):
    class Meta :
        model = OrderItem
        fields = '__all__'


