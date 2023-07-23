from django.core.validators import MinValueValidator
from django.db import models

from users.models import User


class Tag(models.Model):
    name = models.CharField(
        'Name',
        max_length=50,
        unique=True,
    )
    slug = models.SlugField(
        'Slug',
        max_length=50,
        unique=True,
    )
    color = models.CharField(
        'Color',
        max_length=16,
        unique=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Ingredient(models.Model):
    name = models.CharField(
        'Name',
        unique=True,
        max_length=150,
    )
    measurement_unit = models.CharField(
        'Unit',
        max_length=20,
    )

    def __str__(self):
        return f'{self.name} {self.measurement_unit}'

    class Meta:
        ordering = ['name']


class RecipeIngredient(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipeIngredient'
    )
    amount = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1)
        ],
    )

    def __str__(self):
        return (f'{self.ingredient.name}: {self.amount}')


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
    )
    name = models.CharField(
        'Name',
        max_length=50,
        unique=True,
    )
    image = models.ImageField(
        'Image',
        upload_to='recipes/images/',
    )
    text = models.TextField()
    tags = models.ManyToManyField(
        Tag,
    )
    ingredients = models.ManyToManyField(
        RecipeIngredient,
        through='RecipeIngredientRecipe'
    )
    cooking_time = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1)
        ],
    )
    created = models.DateTimeField(auto_now_add=True,
                                   verbose_name='Created')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        ordering = ['-created']


class RecipeIngredientRecipe(models.Model):
    recipe_ingredient = models.ForeignKey(
        RecipeIngredient,
        on_delete=models.CASCADE,
        related_name='recipeIngredientRecipe'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredient'
    )

    def __str__(self):
        return (f'{self.recipe.name} <- ' +
                f'{self.recipe_ingredient.ingredient.name}: ' +
                f'{self.recipe_ingredient.amount}'
                )

    class Meta:
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(
                fields=['recipe_ingredient', 'recipe'],
                name='unique_recipe_ingredient'
            )
        ]


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='infavorite',
    )
    created = models.DateTimeField(auto_now_add=True,
                                   verbose_name='Created')

    def __str__(self):
        return f'{self.user.username} -> {self.recipe.name}'

    class Meta:
        ordering = ['-created']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favorite_recipe'
            )
        ]


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='carts',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='carts'
    )
    created = models.DateTimeField(auto_now_add=True,
                                   verbose_name='Created')

    def __str__(self):
        return f'{self.user.username} -> {self.recipe.name}'

    class Meta:
        ordering = ['-created']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_user_cart'
            )
        ]
