from django import forms
from .models import Recipe

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'steps', 'cooking_time', 'image', 'categories']
        widgets = {
            'categories': forms.CheckboxSelectMultiple(),
            'steps': forms.Textarea(attrs={'rows': 4}),
        }
