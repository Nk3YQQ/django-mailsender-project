run:
	docker-compose up --build -d

entrypoint:
	python3 manage.py migrate
	python3 manage.py csu
	python3 manage.py create_moderator
	python manage.py runserver 0.0.0.0:8000

status:
	docker-compose ps

logs:
	docker-compose logs

linters:
	docker-compose exec -T app flake8 blog/
	docker-compose exec -T app flake8 clients/
	docker-compose exec -T app flake8 mailing/
	docker-compose exec -T app flake8 message/
	docker-compose exec -T app flake8 main/
	docker-compose exec -T app flake8 users/

stop:
	docker-compose down

clean:
	docker-compose down --volumes