run:
	docker-compose up --build -d

entrypoint:
	python3 manage.py migrate
	python3 manage.py csu
	python3 manage.py create_moderator
	python manage.py runserver 0.0.0.0:8000

tests:
	docker-compose exec -T app python3 manage.py test

linters:
	docker-compose exec -T app flake8 mailsender_app/
	docker-compose exec -T app flake8 users/

stop:
	docker-compose down

clean:
	docker-compose down --volumes