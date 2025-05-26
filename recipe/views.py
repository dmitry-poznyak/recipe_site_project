from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.http import HttpResponseForbidden
from django.core.paginator import Paginator
import random
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from .models import Recipe, Category, Favorite
from .forms import RecipeForm


def home(request):
    recipes = list(Recipe.objects.all())

    # Выбор случайных 5 рецептов
    random_recipes = random.sample(recipes, min(len(recipes), 5))

    # Получаем избранные рецепты текущего пользователя
    favorite_recipe_ids = set()
    if request.user.is_authenticated:
        favorite_recipe_ids = set(
            Favorite.objects.filter(user=request.user).values_list('recipe_id', flat=True)
        )

    # Отмечаем, какие из случайных рецептов в избранном
    for recipe in random_recipes:
        recipe.is_favorite = recipe.id in favorite_recipe_ids

    return render(request, 'recipe/home.html', {
        'recipes': random_recipes,
        'favorite_recipes': Recipe.objects.filter(id__in=favorite_recipe_ids)
    })

def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)

    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(user=request.user, recipe=recipe).exists()

    return render(request, 'recipe/recipe_detail.html', {
        'recipe': recipe,
        'is_favorite': is_favorite,
    })


@login_required
def add_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.ingredients = form.cleaned_data.get('ingredients', '')
            recipe.save()
            form.save_m2m()
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
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.ingredients = form.cleaned_data.get('ingredients', '')
            recipe.save()
            form.save_m2m()
            return redirect('recipe_detail', recipe_id=recipe_id)
    else:
        form = RecipeForm(instance=recipe)

    return render(request, 'recipe/edit_recipe.html', {'form': form})


@login_required
def delete_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)

    if recipe.author != request.user:
        return HttpResponseForbidden("Вы не можете удалить этот рецепт.")

    if request.method == "POST":
        recipe.delete()
        return redirect('home')

    return render(request, 'recipe/delete_recipe_confirm.html', {'recipe': recipe})


@login_required
def my_recipes(request):
    recipes = Recipe.objects.filter(author=request.user)
    return render(request, 'recipe/my_recipes.html', {'recipes': recipes})


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


def category_recipes(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    recipes = Recipe.objects.filter(categories=category).prefetch_related('favorited_by')

    # Получаем ID рецептов, добавленных в избранное
    favorite_recipe_ids = set()
    if request.user.is_authenticated:
        favorite_recipe_ids = set(
            Favorite.objects.filter(user=request.user).values_list('recipe_id', flat=True)
        )

    # Помечаем каждый рецепт как избранный или нет
    for recipe in recipes:
        recipe.is_favorite = recipe.id in favorite_recipe_ids

    # Пагинация — 9 рецептов на страницу
    paginator = Paginator(recipes, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'recipe/category_recipes.html', {
        'category': category,
        'page_obj': page_obj,
        'favorite_recipes': Recipe.objects.filter(id__in=favorite_recipe_ids)
    })


def recipe_list(request):
    recipes = Recipe.objects.all().prefetch_related('favorited_by')

    if request.user.is_authenticated:
        favorite_recipe_ids = set(
            Favorite.objects.filter(user=request.user).values_list('recipe_id', flat=True)
        )
    else:
        favorite_recipe_ids = set()

    for recipe in recipes:
        recipe.is_favorite = recipe.id in favorite_recipe_ids

    paginator = Paginator(recipes, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'recipe/recipe_list.html', {
    'page_obj': page_obj,
    'favorite_recipes': Recipe.objects.filter(id__in=favorite_recipe_ids)
})



def categories_context(request):
    categories = Category.objects.all()
    return {'categories': categories}


@login_required
def profile_view(request):
    user_recipes = Recipe.objects.filter(author=request.user)

    favorite_recipe_ids = set(
        Favorite.objects.filter(user=request.user).values_list('recipe_id', flat=True)
    )

    for recipe in user_recipes:
        recipe.is_favorite = recipe.id in favorite_recipe_ids

    favorite_recipes = Recipe.objects.filter(favorited_by__user=request.user)

    for recipe in favorite_recipes:
        recipe.is_favorite = True

    return render(request, 'recipe/profile.html', {
        'user_recipes': user_recipes,
        'favorite_recipes': favorite_recipes,
    })

@login_required
def toggle_favorite(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, recipe=recipe)
    if not created:
        favorite.delete()
    return redirect(request.META.get('HTTP_REFERER', 'home'))


def search_recipes(request):
    query = request.GET.get('q')
    recipes = Recipe.objects.filter(title__icontains=query).prefetch_related('favorited_by') if query else []

    favorite_recipe_ids = set()
    if request.user.is_authenticated:
        favorite_recipe_ids = set(
            Favorite.objects.filter(user=request.user).values_list('recipe_id', flat=True)
        )

    for recipe in recipes:
        recipe.is_favorite = recipe.id in favorite_recipe_ids

    return render(request, 'recipe/search_results.html', {
        'recipes': recipes,
        'query': query,
        'favorite_recipes': Recipe.objects.filter(id__in=favorite_recipe_ids)
    })

