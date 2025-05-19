from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('recipe/<int:recipe_id>/', views.recipe_detail, name='recipe_detail'),
    path('recipe/add/', views.add_recipe, name='add_recipe'),
    path('recipe/<int:recipe_id>/edit/', views.edit_recipe, name='edit_recipe'),
    path('signup/', views.signup_view, name='signup'),
    path('category/<int:category_id>/', views.category_recipes, name='category_recipes'),

     # регистрация
    path('register/', views.register, name='register'),

    # встроенные представления Django для логина/логаута
    path('login/', auth_views.LoginView.as_view(template_name='recipe/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
]
