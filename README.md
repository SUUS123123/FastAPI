# Computer Shop API

FastAPI-приложение магазина компьютеров, организованное по слоям: API, сервисы, репозитории, модели и схемы.

## Запуск

1. Убедитесь, что запущен SQL Server, создана база `ComputerShop`, установлен Microsoft ODBC Driver 18 for SQL Server.
2. Активируйте окружение в PowerShell: `\.venv\Scripts\Activate.ps1`.
3. Установите зависимости при необходимости: `pip install -r requirements.txt`.
4. Запустите сервер: `uvicorn main:app --reload`.
5. Откройте `http://127.0.0.1:8000` или документацию `http://127.0.0.1:8000/docs`.

Параметры SQL Server задаются в `.env`. Для SQL-аутентификации установите `DB_TRUSTED_CONNECTION=no`, `DB_USER` и `DB_PASSWORD`.

## Структура

- `main.py` — создание FastAPI-приложения и точка входа.
- `app/config.py`, `app/database.py` — настройки и подключение к БД.
- `app/models/` — таблицы SQLAlchemy.
- `app/schemas/` — схемы запросов и ответов Pydantic.
- `app/repositories/` — операции чтения и записи в БД.
- `app/services/` — бизнес-логика.
- `app/api/v1/` — HTTP-маршруты API.
- `static/` — веб-интерфейс магазина.
