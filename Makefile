runserver:
	python3 manage.py runserver

docker-compose-run:
	docker-compose up -d

tests:
	docker-compose exec -T app python3 manage.py test

clean-up:
	docker-compose down --volumes