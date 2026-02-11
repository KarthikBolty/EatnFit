from django import forms
from .models import Meal

class MealForm(forms.ModelForm):
    class Meta:
        model = Meal
        fields = ['meal_type', 'food_name', 'calories']
        widgets = {
            'meal_type': forms.Select(attrs={'class': 'form-select'}),
            'food_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter food name'}),
            'calories': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter calories'})
        }
