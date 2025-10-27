# Мобильное приложение и REST API для отправки данных о перевалах

Проект включает мобильное приложение для Android и iOS, а также REST API на Django, разработанные для упрощения отправки туристами данных о перевалах в Федерацию спортивного туризма России (ФСТР). Приложение позволяет вносить данные в горах и отправлять их при появлении интернета.
## Описание проекта
- **Мобильное приложение**: Для Android и iOS. Пользователи вводят данные о перевале (координаты, высота, имя, почта, телефон, название, фото) и отправляют их в ФСТР через API.
- **REST API**: Backend на Django для хранения и управления данными в базе данных. При добавлении новой записи статус устанавливается как "new".

## Функции
- Сбор и отправка данных о перевалах: координаты, высота, пользовательские данные, название, фото.
- Хранение данных в БД с модерацией (статус: new, pending, accepted и т.д.).
- API для CRUD операций: получение, редактирование (только для статуса "new"), фильтрация по email.

## Что было реализовано
- **Модель данных**: Классы Django для хранения перевалов и связанных данных (пользователи, фото).
- **REST API**: Методы для работы с данными:
  - Добавление нового перевала (POST).
  - Получение записи по ID (GET).
  - Редактирование записи (PATCH, только если статус "new").
  - Получение списка данных обо всех объектах, которые пользователь с почтой <email> отправил на сервер (GET с фильтром).

## Установка и запуск
### Для REST API (Django)
1. Клонируйте репозиторий: `git clone https://github.com/Yulish/the_probation.git`
2. Установите зависимости: `pip install -r requirements.txt`
3. Настройте базу данных в `settings.py` (например, PostgreSQL). Путь к базе данных берётся из переменных окружения операционной системы: FSTR_DB_HOST, FSTR_DB_PORT, FSTR_LOGIN, FSTR_PASS. Создайте файл .env в корне проекта и добавьте следующие переменные, например:
FSTR_DB_HOST=localhost
FSTR_DB_PORT=5432
FSTR_LOGIN=your_db_user
FSTR_PASS=your_db_password

4. Запустите миграции: `python manage.py migrate`
5. Запустите сервер: `python manage.py runserver` (локально: `http://127.0.0.1:8000/`)
6. Для продакшена: Задеплойте на сервер (например, Yandex Cloud), используя Docker или напрямую.

### Для мобильного приложения
- Скачайте APK для Android или IPA для iOS из релизов репозитория.
- Установите на устройство и настрой доступ к интернету для отправки данных.

## API Endpoints
Базовый URL: `http://127.0.0.1:8000/api/submitData/`.

### Основные правила
- Все запросы в формате JSON.
- Методы: GET (чтение), POST (создание), PATCH (обновление).
- Статусы: 200 OK (успех), 400 Bad Request (ошибка), 404 Not Found (не найдено), 405 Method Not Allowed (метод не разрешён).

### Детали endpoints
- **POST /api/submitData/**: Добавить новый перевал.
  - Тело: `"beautyTitle": "перевалище ", "title": "Отдых", "other_titles": "Очередной перевал", "user": { "email": "test@mail.ru", "fio": "Иванов Иван Иванович", "phone": "+7 666 66 66"},{"coords": {"latitude": 45.0, "longitude": 37.0, "height": 1000}, "level": {"winter": "4B", "summer": "1А", "autumn": "2А", "spring": "3B"},"images": [{ "title": "Очередной перевал","data":["url1.jpg", "url2.jpg"]}`
  - Ответ: `{"id": 1, "status": "new"}` (статус автоматически "new").
- **GET /api/submitData/<id>/**: Получить одну запись по ID (включая статус модерации).
  - Пример ответа: `{"id": 1, "coords": {...}, "user": {...}, "title": "Перевал", "images": [...], "status": "new"}`
- **PATCH /api/submitData/<id>/**: Редактировать запись (только если статус "new").
  - Тело: `{"title": "Новое название"}`
  - Ответ: `{"state": 1, "message": "Запись обновлена"}` (state=1 — успех, state=0 — ошибка с message, например "Статус не new").
- **GET /api/submitData/?user__email=<email>**: Получить список записей пользователя по email.
  - Пример: `/api/submitData/?user__email=ivan@example.com`
  - Ответ: `[{"id": 1, "title": "Перевал 1"}, {"id": 2, "title": "Перевал 2"}]`

## Примеры запросов
### С помощью curl
- Добавить перевал: `curl -X POST -H "Content-Type: application/json" -d '{"coords":{"latitude":45.0,"longitude":37.0,"height":1000},"user":{"name":"Иван","email":"ivan@example.com","phone":"+7-999-123-45-67"},"title":"Мой перевал","images":["photo1.jpg"]}' http://127.0.0.1:8000/api/submitData/`
- Получить запись: `curl http://127.0.0.1:8000/api/submitData/1/`
- Редактировать: `curl -X PATCH -H "Content-Type: application/json" -d '{"title":"Обновлённый перевал"}' http://127.0.0.1:8000/api/submitData/1/`
- Список по email: `curl "http://127.0.0.1:8000/api/submitData/?user__email=ivan@example.com"`

### С помощью Python (requests)
```python
import requests

# Добавить перевал
url = "http://127.0.0.1:8000/api/submitData/"
data = {
    "coords": {"latitude": 45.0, "longitude": 37.0, "height": 1000},
    "user": {"name": "Иван", "email": "ivan@example.com", "phone": "+7-999-123-45-67"},
    "title": "Мой перевал",
    "images": ["photo1.jpg"]
}
response = requests.post(url, json=data)
print(response.json())

# Получить запись
response = requests.get(f"{url}1/")
print(response.json())
```

## Ошибки и статусы
- 400: Неверные данные (проверь JSON).
- 404: Запись не найдена.
- 405: Метод не разрешён (например, PATCH для не-new статуса).
- Для PATCH: Если state=0, message укажет причину (например, "Запись не в статусе new").

## Тестирование
- Используйте Postman для тестирования endpoints.
– Тестируйте мобильное приложение на устройстве с симуляцией оффлайн-режима.

## Контакты
Автор: Мурсалимова Юлия Рамильевна. Email: ishmakova1@yandex.ru. Репозиторий: [GitHub](https://github.com/Yulish/the_probation.git).