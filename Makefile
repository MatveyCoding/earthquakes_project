.PHONY: up down logs psql restart clean

up:
	docker-compose up -d
down:
	docker-compose down
restart:
	docker-compose restart
logs:
	docker-compose logs -f
	
producer:
	docker exec -it airflow-scheduler python -m src.messaging.producer

consumer:
	docker exec -it airflow-scheduler python -m src.messaging.consumer