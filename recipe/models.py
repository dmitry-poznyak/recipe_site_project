from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Recipe(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    steps = models.TextField()
    cooking_time = models.PositiveIntegerField()
    image = models.ImageField(upload_to='recipes/')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes')

    categories = models.ManyToManyField(Category, blank=True, related_name='recipes')


    def __str__(self):
        return self.title


