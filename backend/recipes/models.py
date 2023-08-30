from django.core.validators import (MinValueValidator, MaxValueValidator)
from django.db import models

from users.models import User


MIN_VALUE = 1
MAX_VALUE = 32000


class Tag(models.Model):
    name = models.CharField(
        'Название',
        max_length=50,
        unique=True,
    )
    slug = models.SlugField(
        'Slug',
        max_length=50,
        unique=True,
    )
    color = models.CharField(
        'Цвет',
        max_length=16,
        unique=True,
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        'Название',
        max_length=150,
    )
    measurement_unit = models.CharField(
        'ед. изм.',
        max_length=20,
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'{self.name} {self.measurement_unit}'


class RecipeIngredient(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipeIngredient',
        verbose_name='Ингредиент'
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        validators=[
            MinValueValidator(MIN_VALUE),
            MaxValueValidator(MAX_VALUE)
        ],
    )

    class Meta:
        ordering = ['id']

    def __str__(self):
        return (f'{self.ingredient.name}: {self.amount}')


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор',
    )
    name = models.CharField(
        'Название',
        max_length=50,
        unique=True,
    )
    image = models.ImageField(
        'Изображение',
        upload_to='recipes/images/',
    )
    text = models.TextField(
        verbose_name='Описание',
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги',
    )
    ingredients = models.ManyToManyField(
        RecipeIngredient,
        verbose_name='Ингредиент с кол.',
        through='RecipeIngredientRecipe'
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления',
        validators=[
            MinValueValidator(MIN_VALUE),
            MaxValueValidator(MAX_VALUE)
        ],
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Создан',
    )

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'{self.name}'


class RecipeIngredientRecipe(models.Model):
    recipe_ingredient = models.ForeignKey(
        RecipeIngredient,
        on_delete=models.CASCADE,
        related_name='recipeIngredientRecipe',
        verbose_name='Ингредиент с кол.',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredient',
        verbose_name='Рецепт',
    )

    class Meta:
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(
                fields=['recipe_ingredient', 'recipe'],
                name='unique_recipe_ingredient'
            )
        ]

    def __str__(self):
        return (f'{self.recipe.name} <- '
                + f'{self.recipe_ingredient.ingredient.name}: '
                + f'{self.recipe_ingredient.amount}'
                )


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='infavorite',
        verbose_name='Рецепт',
    )
    created = models.DateTimeField(auto_now_add=True,
                                   verbose_name='Создан')

    class Meta:
        ordering = ['-created']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favorite_recipe'
            )
        ]

    def __str__(self):
        return f'{self.user.username} -> {self.recipe.name}'


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='carts',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='carts',
        verbose_name='Рецепт',
    )
    created = models.DateTimeField(auto_now_add=True,
                                   verbose_name='Создан')

    class Meta:
        ordering = ['-created']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_user_cart'
            )
        ]

    def __str__(self):
        return f'{self.user.username} -> {self.recipe.name}'
