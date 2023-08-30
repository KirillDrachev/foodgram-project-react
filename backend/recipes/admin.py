from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                     RecipeIngredientRecipe, ShoppingCart, Tag)


class IngredientResource(resources.ModelResource):

    class Meta:
        model = Ingredient
        import_id_fields = ('name',)
        skip_unchanged = True


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


class RecipeIngredientInLine(admin.TabularInline):
    model = RecipeIngredientRecipe
    extra = 0
    min_num = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('author', 'name')
    list_filter = ('author', 'tags')
    inlines = (RecipeIngredientInLine, )


@admin.register(Favorite)
class Favourite(admin.ModelAdmin):
    exclude = ('pk',)


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    exclude = ('pk',)
    search_fields = ('user', 'recipe')
