from django.contrib import admin

from .models import (Ingredient, Tag, Recipe,
                     Favorite, ShoppingCart, RecipeIngredient, RecipeIngredients)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    exclude = ('pk',)


@admin.register(RecipeIngredient)
class RecipeIngredienttAdmin(admin.ModelAdmin):
    exclude = ('pk',)

@admin.register(RecipeIngredients)
class RecipeIngredienttAdmin(admin.ModelAdmin):
    exclude = ('pk',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    exclude = ('pk',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('author', 'name')
    list_filter = ('author', 'tags')



@admin.register(Favorite)
class Favourite(admin.ModelAdmin):
    exclude = ('pk',)


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    exclude = ('pk',)
    search_fields = ('user', 'recipe')
