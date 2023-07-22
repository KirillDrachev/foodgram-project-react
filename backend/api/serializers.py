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
    
class TagListSerializer(serializers.ListSerializer):
    index_field = 'pk'
class TagSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    name = serializers.CharField(required=False)
    slug = serializers.SlugField(required=False)
    color = serializers.CharField(required=False)
    class Meta:
        model = Tag
        fields = ('id', 'name', 'slug', 'color')
        list_serializer_class = TagListSerializer

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
    # tags = TagSerializer(many=True, )
    tags = serializers.PrimaryKeyRelatedField(many=True, required=True, read_only=False, queryset=Tag.objects.all(), )
    ingredients = RecipeIngredientSerializer(many=True, read_only=False)
    author = UserSerializer(read_only=True)

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients',
                  'name',
                  'image', 'text', 'cooking_time',)
        depth = 1

    def validate(self, data):
        print(data.get('tags'))
        # tag_id_list = []
        # for tag_id in data.get('tags'):
        #     print(tag_id)
        #     tag_id_list.append({'id': tag_id})
        # print(tag_id_list)
        # data.get('tags').set(tag_id_list)
        return data
    
    def create(self, validated_data):
        request = self.context.get('request')
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(author=request.user, **validated_data)
        recipe.tags.set(tags)
        for ingredient in ingredients:

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
    
    def update(self,instance, validated_data):
        request = self.context.get('request')
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        instance.tags.clear()
        instance.tags.set(tags)
        instance.ingredients.all().delete()
        for ingredient in ingredients:
            current_ingredient = get_object_or_404(
                Ingredient, id=ingredient.get('ingredient').get('id')
            )
            amount = ingredient.get('amount')
            current_recipe_ingredient = RecipeIngredient.objects.create(
                ingredient=current_ingredient, amount=amount
            )
            RecipeIngredients.objects.create(
                recipe_ngredient=current_recipe_ingredient, recipe=instance
            )
        instance.save()
        return instance
    

class RecipeGetSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    tags = TagSerializer(many=True, read_only=True)
    ingredients = RecipeIngredientSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients',
                  'name',
                  'image', 'text', 'cooking_time',)

   