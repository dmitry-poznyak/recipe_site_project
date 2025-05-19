from django.shortcuts import render, get_object_or_404, redirect
from .models import Recipe, Category
from .forms import RecipeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.http import HttpResponseForbidden
from django.core.paginator import Paginator
import random


def home(request):
    recipes = list(Recipe.objects.all())
    random_recipes = random.sample(recipes, min(len(recipes), 5))
    return render(request, 'recipe/home.html', {'recipes': random_recipes})

def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    return render(request, 'recipe/recipe_detail.html', {'recipe': recipe})

@login_required
def add_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)  # Не сохраняем сразу
            recipe.author = request.user      # Устанавливаем автора
            recipe.save()                     # Теперь сохраняем
            form.save_m2m()                   # Сохраняем связи many-to-many
            return redirect('recipe_detail', recipe_id=recipe.id)
    else:
        form = RecipeForm()
    return render(request, 'recipe/add_recipe.html', {'form': form})

@login_required
def edit_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)

    if recipe.author != request.user:
        return HttpResponseForbidden("Вы не можете редактировать этот рецепт.")

    if request.method == 'POST':
        form = RecipeForm(request.POST, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect('recipe_detail', recipe_id=recipe_id)
    else:
        form = RecipeForm(instance=recipe)

    return render(request, 'recipe/edit_recipe.html', {'form': form})

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'recipe/signup.html', {'form': form})

def category_recipes(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    recipes = category.recipes.all()
    return render(request, 'recipe/category_recipes.html', {
        'category': category,
        'recipes': recipes
    })

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'recipe/register.html', {'form': form})

@login_required
def delete_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)

    # Проверяем, что текущий пользователь — автор рецепта
    if recipe.author != request.user:
        return HttpResponseForbidden("Вы не можете удалить этот рецепт.")

    if request.method == "POST":
        recipe.delete()
        return redirect('home')

    # Если GET — можно показать подтверждение удаления (опционально)
    return render(request, 'recipe/delete_recipe_confirm.html', {'recipe': recipe})

def recipe_list(request):
    recipe_list = Recipe.objects.all()
    paginator = Paginator(recipe_list, 9)  # 9 рецептов на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'recipe/recipe_list.html', {'page_obj': page_obj})

@login_required
def my_recipes(request):
    recipes = Recipe.objects.filter(author=request.user)
    return render(request, 'recipe/my_recipes.html', {'recipes': recipes})

def categories_context(request):
    categories = Category.objects.all()
    return {'categories': categories}
