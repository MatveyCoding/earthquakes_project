# Earthquake pipeline

## Цель
Пайплайн для сбора и анализа данных о землетрясениях

## Архитектура
USGS API → Kafka → PostgreSQL → Pandas (аналитика) → BI
                    (Airflow)

## Описание компонентов
### Оркестрация
- **Airflow** - оркестратор 
### Пайплайн
- **Producer** - забирает данные с API и отправляет в Kafka
- **Consumer** - читает данные из Kafka и сохраняет в PostgreSQL
- **Pandas** - агрегации
### Инфраструктура
- **Kafka** - транспорт сообщений
- **PostgreSQL** - База данных
- **Docker** - контейнеризация
## DAG и Airflow

| DAG | Периодичность | Действие |
| `earthquake_producer` | каждые 5 минут | Запускает producer |
| `earthquake_consumer` | каждые 5 минут | Запускает consumer |
| `earthquake_analytics`| раз в час| Агрегирует данные |

## Запуск

## Конфигурация