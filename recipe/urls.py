from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('recipe/<int:recipe_id>/', views.recipe_detail, name='recipe_detail'),
    path('recipe/add/', views.add_recipe, name='add_recipe'),
    path('recipe/<int:recipe_id>/edit/', views.edit_recipe, name='edit_recipe'),
    path('recipe/<int:pk>/delete/', views.delete_recipe, name='delete_recipe'),
    path('signup/', views.signup_view, name='signup'),
    path('category/<int:category_id>/', views.category_recipes, name='category_recipes'),
    path('recipes/', views.recipe_list, name='recipe_list'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='recipe/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('my/', views.my_recipes, name='my_recipes'),
    path('profile/', views.profile_view, name='profile'),
    path('favorite/<int:recipe_id>/', views.toggle_favorite, name='toggle_favorite'),
    path('search/', views.search_recipes, name='search_recipes'),
]
