# Earthquake pipeline

## Цель
Пайплайн для сбора и анализа данных о землетрясениях

## Архитектура
USGS API → Kafka → Airflow → PostgreSQL → Metabase(BI)
              

## Описание компонентов

### Оркестрация
- **Airflow** - оркестратор 

### Инфраструктура
- **Kafka** - транспорт сообщений
- **PostgreSQL** - База данных
- **Docker** - контейнеризация

## DAG и Airflow
| Оператор| Периодичность | Действие |
|-----|---------------|----------|
| `task_producer` | каждые 2 часа | Запускает producer API землетрясений |
| `task_consumer` | каждые 2 часа | Запускает consumer  API землетрясений |
| `task_producer_weather`|  каждые 2 часа | Запускает producer  API погоды|
| `task_consumer_weather`|  каждые 2 часа | Запускает consumer  API погоды|
| `join_task`|  каждые 2 часа | Соединяет таблицы погоды и землетрясений|

## Запуск
1. Клонируем репозиторий;
2. Переходим в папку с проектом: cd earthquakes_project;
3. Создаём .env: cp .env.example .env;
4. Заполняем переменную OPENWEATHER_API_KEY и при необходимости AIRFLOW_UID;
5. Проверяем, что докер запущен и запускаем docker-compose up -d;
6. Открываем Airflow и запускаем DAG;
7. Открываем Metabase, регистрируемся и снабжаем дашбродами;

## Состав сервисов:
- **Airflow** - http://localhost:8081 (admin/admin)

- **Kafka UI** - http://localhost:8080

- **Metabase(BI)** - http://localhost:3000