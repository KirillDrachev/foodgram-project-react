import base64

from django.core.files.base import ContentFile
from djoser.serializers import UserCreateSerializer
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from recipes.models import (Ingredient, Tag, Favorite,
                            Recipe, RecipeIngredient, RecipeIngredients, ShoppingCart)
from users.models import User, Subscribe

class UserSerializer(UserCreateSerializer):
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta(UserCreateSerializer.Meta):
        fields = (
            'username', 'id', 'email', 'first_name', 'last_name', 'password',
            'is_subscribed',
        )
        extra_kwargs = {'password': {'write_only': True}}
        model = User

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        return (request.user.is_authenticated
                and request.user.follower.filter(author=obj).exists())
    

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)
    

        
class IngredientGetSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='ingredient.id', read_only=True)
    name = serializers.CharField(source='ingredient.name', read_only=True)
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit',
        read_only=True
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')



class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='ingredient.id', )
    name = serializers.CharField(source='ingredient.name',read_only=True , required=False)
    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=True)
    tags = TagSerializer(many=True, required=False)
    ingredients = RecipeIngredientSerializer(many=True, )
    author = UserSerializer(read_only=True)

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients',
                  'name',
                  'image', 'text', 'cooking_time',)

    def create(self, validated_data):
        request = self.context.get('request')
        print(self.initial_data)
        print(self.validated_data)
        if 'ingredients' not in self.initial_data:
            recipe = Recipe.objects.create(author=request.user, **validated_data)
            return recipe
        ingredients = validated_data.pop('ingredients')
        print(ingredients)
        recipe = Recipe.objects.create(author=request.user, **validated_data)
        for ingredient in ingredients:
            print(ingredient)
            print(ingredient.get('ingredient').get('id'))
            current_ingredient = get_object_or_404(
                Ingredient, id=ingredient.get('ingredient').get('id')
            )
            amount = ingredient.get('amount')
            current_recipe_ingredient = RecipeIngredient.objects.create(
                ingredient=current_ingredient, amount=amount
            )
            RecipeIngredients.objects.create(
                recipe_ngredient=current_recipe_ingredient, recipe=recipe
            )
        return recipe