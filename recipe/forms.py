from django import forms
from .models import Recipe, Category, Ingredient

class RecipeForm(forms.ModelForm):
    ingredients_text = forms.CharField(
        label='Ингредиенты (через запятую)',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
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
            'categories': 'Категории',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            ingredients_qs = self.instance.ingredients.all()
            self.fields['ingredients_text'].initial = ', '.join([i.name for i in ingredients_qs])

    def save(self, commit=True):
        recipe = super().save(commit=False)
        if commit:
            recipe.save()
            self.save_m2m()
            # обновим ингредиенты
            ingredients_text = self.cleaned_data.get('ingredients_text', '')
            if ingredients_text:
                ingredient_names = [i.strip() for i in ingredients_text.split(',') if i.strip()]
                # Очистим старые ингредиенты
                recipe.ingredients.clear()
                for name in ingredient_names:
                    ingredient, created = Ingredient.objects.get_or_create(name=name)
                    recipe.ingredients.add(ingredient)
        return recipe
