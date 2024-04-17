run:
	python3 manage.py runserver 8001
migrations:
	python3 manage.py makemigrations
migrations-catalog:
	python3 manage.py makemigrations catalog
migrate:
	python3 manage.py migrate
superuser:
	python3 manage.py createsuperuser
dumpdata:
	python manage.py dumpdata > locallibrary.json
loaddata:
	python manage.py loaddata locallibrary.json
clean:
	rm -r catalog/migrations
collstatic:
	python manage.py collectstatic