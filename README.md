# Сервис авторизации по номеру телефона

Реферальная система с авторизацией по номеру телефона и инвайт-кодами.

## Стек

- Python 3.12
- Django 6.0
- Django REST Framework
- PostgreSQL
- Docker + Docker Compose
- JWT авторизация

## Запуск локально

1. Клонировать репозиторий:
   ```bash
   git clone https://github.com/KirlRj/Graduate_work.git
   cd Graduate_work
   ```

2. Создать виртуальное окружение и установить зависимости:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Создать `.env` файл по шаблону `.env.example` и заполнить переменные

4. Создать базу данных PostgreSQL:
   ```sql
   psql -U postgres
   CREATE DATABASE graduate_work;
   ```

5. Применить миграции:
   ```bash
   python manage.py migrate
   ```

6. Запустить сервер:
   ```bash
   python manage.py runserver
   ```

## Запуск через Docker

1. Создать `.env` файл по шаблону `.env.example` (DATABASE_HOST=db)

2. Запустить:
   ```bash
   docker-compose up --build
   ```

3. Применить миграции:
   ```bash
   docker-compose exec web python manage.py migrate
   ```

4. Приложение доступно на `http://localhost:8000`

## Интерфейс

- Главная страница: `http://localhost:8000/users/`
- Документация Swagger: `http://localhost:8000/api/docs/`
- Документация ReDoc: `http://localhost:8000/api/redoc/`

## API

### Отправка кода подтверждения

```
POST /users/send-code/
```

Запрос:
```json
{"phone": "89991234567"}
```

Ответ:
```json
{"message": "Код подтверждения отправлен на номер 89991234567"}
```

### Верификация кода

```
POST /users/verify-code/
```

Запрос:
```json
{"phone": "89991234567", "code": "1234"}
```

Ответ:
```json
{
    "access": "eyJ...",
    "refresh": "eyJ..."
}
```

### Профиль пользователя

```
GET /users/profile-view/
Authorization: Bearer <access_token>
```

Ответ:
```json
{
    "phone": "89991234567",
    "referral_code": "ABC123",
    "users_referral_code": null,
    "referrals": []
}
```

### Активация инвайт-кода

```
POST /users/profile-view/
Authorization: Bearer <access_token>
```

Запрос:
```json
{"referral_code": "XYZ999"}
```

Ответ:
```json
{"message": "Инвайт-код активирован"}
```

## Тесты

```bash
python manage.py test
```

Покрытие тестами: 79%
