from django import forms
from .models import Recipe, Category


class RecipeForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        label='Категория',
        required=False
    )

    class Meta:
        model = Recipe
        fields = ['title', 'description', 'steps', 'cooking_time', 'image', 'categories']
        labels = {
            'title': 'Название',
            'description': 'Описание',
            'steps': 'Шаги приготовления',
            'cooking_time': 'Время приготовления (минуты)',
            'image': 'Изображение',
        }
        widgets = {
            'steps': forms.Textarea(attrs={'rows': 4}),
        }
