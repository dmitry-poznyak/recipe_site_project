from django import forms
from .models import Recipe, Category


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'steps', 'cooking_time', 'image', 'categories']
        labels = {
            'title': 'Название',
            'description': 'Описание',
            'steps': 'Шаги приготовления',
            'cooking_time': 'Время приготовления (минуты)',
            'image': 'Изображение',
            'categories': 'Категория',
        }
        widgets = {
            'categories': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'steps': forms.Textarea(attrs={'rows': 4}),
        }
