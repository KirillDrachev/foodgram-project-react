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
- Выполнить команды миграции, создания супер пользователя и сбора статики:
- sudo docker exec foodgram-project-react-backend-1 python manage.py migrate --run-syncdb
- sudo docker exec foodgram-project-react-backend-1 python manage.py collectstatic
- sudo docker exec foodgram-project-react-backend-1 cp -r /app/backend_static/. /backend_static/static/
- sudo docker exec -it foodgram-project-react-backend-1 python3 manage.py createsuperuser
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