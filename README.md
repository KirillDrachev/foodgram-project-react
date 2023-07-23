# praktikum_new_diplom
Осталось 3 дня, сразу решил развернуть на сревере 

http://158.160.62.106/recipes

superuser:
kirill
kirill@kirill.com
kirill




sudo docker exec foodgram-project-react-backend-1 python manage.py migrate --run-syncdb

sudo docker exec foodgram-project-react-backend-1 python manage.py collectstatic
sudo docker exec foodgram-project-react-backend-1 cp -r /app/backend_static/. /backend_static/static/
sudo docker exec -it foodgram-project-react-backend-1 python3 manage.py createsuperuser