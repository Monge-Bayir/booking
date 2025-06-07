# 🏨 FastAPI Hotel Booking API

**Проект бронирования отелей** на FastAPI с поддержкой JWT-аутентификации, PostgreSQL, Alembic и Docker.

## 🚀 Возможности

- Регистрация и аутентификация пользователей
- Бронирование номеров в отелях
- Просмотр отелей, номеров и изображений
- Использование HTML-шаблонов (Jinja2)
- Асинхронная работа с базой данных (SQLAlchemy + asyncpg)

## 🗂️ Структура
```
.
├── app/
│ ├── main.py # Точка входа
│ ├── config.py # Настройки проекта
│ ├── database.py # Подключение к БД
│ ├── booking/ # Бронирование
│ ├── hotels/ # Отели
│ ├── rooms/ # Номера
│ ├── users/ # Пользователи и авторизация
│ ├── pages/ # HTML-страницы
│ ├── images/ # Работа с изображениями
│ ├── dao/ # Общие DAO-классы
│ ├── static/ # Статика
│ ├── templates/ # Jinja2-шаблоны
│ └── migrations/ # Alembic миграции
├── .env # Переменные окружения
├── alembic.ini # Конфигурация Alembic
├── requirements.txt # Зависимости
├── Dockerfile
└── docker-compose.yml
```

## 🧪 Локальный запуск

### 1. Клонировать и перейти в папку проекта

```bash
git clone https://github.com/Monge-Bayir/booking.git
```
### 2. Создать .env файл
```
DATABASE_URL=postgresql+asyncpg://user:password@db:5432/hotel_booking
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```
### 3. Собрать и запустить контейнеры
```
docker-compose up --build
```
Приложение будет доступно по адресу: http://localhost:8000
### 4. Применить миграции
```
docker exec -it fastapi_app alembic upgrade head
```
### 🐳 Docker
```
FastAPI + Uvicorn
PostgreSQL
Alembic
Все в одном docker-compose
```
