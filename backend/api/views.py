from django.shortcuts import HttpResponse, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from api.filters import RecipeFilter
from api.permissions import IsAuthorOrReadOnly
from recipes.models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                            ShoppingCart, Tag)
from users.models import Subscribe, User

from .serializers import (FavoriteSerializer, IngredientSerializer,
                          RecipeGetSerializer, RecipeSerializer,
                          ShoppingCartSerializer, TagSerializer,
                          UserSubscribeSerializer, UserSubscribeViewSerializer)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)
    pagination_class = None
    http_method_names = ['get', ]


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny, )
    pagination_class = None
    http_method_names = ['get', ]

    def get_queryset(self):
        if (self.request.query_params.get('name')):
            return Ingredient.objects.filter(
                name__startswith=self.request.query_params.get('name'))
        return Ingredient.objects.all()


class RecipeViewSet(viewsets.ModelViewSet):
    # queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    permission_classes = [IsAuthorOrReadOnly, ]
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        if (self.request.query_params.get('is_favorited') == '1'):
            print("is_favorited")
            return Recipe.objects.filter(infavorite__user=self.request.user)
        elif (self.request.query_params.get('is_in_shopping_cart') == '1'):
            return Recipe.objects.filter(carts__user=self.request.user)
        elif (self.request.query_params.get('author')):
            return Recipe.objects.filter(
                author=self.request.query_params.get('author'))
        else:
            return Recipe.objects.all()

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeGetSerializer
        return RecipeSerializer

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated, ]
    )
    def shopping_cart(self, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == 'POST':
            serializer = ShoppingCartSerializer(
                data={'user': request.user.id, 'recipe': recipe.id, },
                context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            get_object_or_404(ShoppingCart, user=request.user,
                              recipe=recipe).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=['get'],
        permission_classes=[IsAuthenticated, ]
    )
    def download_shopping_cart(self, request):
        ingredients_list = []
        recipes = Recipe.objects.filter(carts__user=request.user)
        for recipe in recipes:
            ingredients = RecipeIngredient.objects.filter(
                recipeIngredientRecipe__recipe=recipe
            )
            for ingredient in ingredients:
                ingredients_list.append(
                    [
                        ingredient.ingredient.name,
                        ingredient.amount,
                        ingredient.ingredient.measurement_unit
                    ]
                )
        shopping_cart = []
        for ingredient in ingredients_list:
            name = ingredient[0]
            unit = ingredient[2]
            amount = ingredient[1]
            shopping_cart.append(f'\n{name} - {amount}, {unit}')
        response = HttpResponse(shopping_cart, content_type='text/plain')
        response[
            'Content-Disposition'
        ] = 'attachment; filename="shopping_cart.txt"'
        return response

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated, ]
    )
    def favorite(self, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)

        if request.method == 'POST':
            serializer = FavoriteSerializer(
                data={'user': request.user.id, 'recipe': recipe.id, },
                context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            get_object_or_404(Favorite, user=request.user,
                              recipe=recipe).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class UserSubscriptionsGetViewSet(viewsets.ModelViewSet):
    serializer_class = UserSubscribeViewSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        return User.objects.filter(following__user=self.request.user)


class UserSubscriptionsViewSet(viewsets.ModelViewSet):
    serializer_class = UserSubscribeSerializer
    permission_classes = [IsAuthenticated, ]
    queryset = Subscribe.objects.all()

    def post(self, request, user_id):
        author = get_object_or_404(User, id=user_id)
        serializer = UserSubscribeSerializer(
            data={'user': request.user.id, 'author': author.id},
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, user_id):
        subscriotion = get_object_or_404(Subscribe, user=request.user.id,
                                         author=user_id
                                         )
        subscriotion.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
