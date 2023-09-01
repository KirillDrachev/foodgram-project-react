# Foodgram
Проект предоставляет возможность обмениваться рецептами блюд, 
создавать новые, добавлять в избранное и 
генерировать список покупок для выбранных рецептов.

## Подключение
- Расположение сервера: http://158.160.62.106/recipes
### superuser
- username: kirill
- mail: kirill@kirill.com
- password: kirill

## Установка
- Скачать репозиторий
- Запустить docker compose up docker-compose.yml

## Примеры запросов

- POST http://127.0.0.1:8000/api/recipes/

{
  "ingredients": [
    {
      "id": 1,
      "amount": 10
    }
  ],
  "tags": [
    1
  ],
  "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
  "name": "strieednedcdrededesxsxswg",
  "text": "string",
  "cooking_time": 1
}

- POST http://127.0.0.1:8000/api/recipes/1/favorite/
- GET http://127.0.0.1:8000/api/recipes/

## Автор
- Драчев Кирилл