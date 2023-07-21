from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny

from recipes.models import (Ingredient, Tag, Recipe,
                            Favorite, RecipeIngredient, ShoppingCart)
from users.models import User, Subscribe
from .serializers import (IngredientSerializer, TagSerializer, RecipeSerializer)

class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny, )
    search_fields = ('^name',)
    pagination_class = None

class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes=[IsAuthenticated, ]
    http_method_names = ['get', 'post', 'patch', 'delete']

    # def perform_create(self, serializer):
    #     serializer.save(author=self.request.user)