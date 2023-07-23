from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                     RecipeIngredientRecipe, ShoppingCart, Tag)


# @admin.register(Ingredient)
# class IngredientAdmin(admin.ModelAdmin):
#     exclude = ('pk',)

class IngredientResource(resources.ModelResource):

    class Meta:
        model = Ingredient


class IngredientAdmin(ImportExportModelAdmin):
    resource_classes = [IngredientResource]


admin.site.register(Ingredient, IngredientAdmin)


@admin.register(RecipeIngredient)
class RecipeIngredienttAdmin(admin.ModelAdmin):
    exclude = ('pk',)


@admin.register(RecipeIngredientRecipe)
class RecipeIngredienttRecipeAdmin(admin.ModelAdmin):
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
