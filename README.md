# Computer Shop API

Учебное приложение магазина компьютеров: FastAPI, SQLAlchemy и SQL Server. Веб-интерфейс открывается на `/`, интерактивная документация API — на `/docs`.

## Запуск на новом компьютере

Понадобятся Windows, Python 3.10 или новее, Git, SQL Server Express и Microsoft ODBC Driver 18 for SQL Server. Для выполнения SQL-файла удобно установить SQL Server Management Studio (SSMS).

- [SQL Server Express](https://www.microsoft.com/sql-server/sql-server-downloads)
- [Microsoft ODBC Driver 18](https://learn.microsoft.com/sql/connect/odbc/download-odbc-driver-for-sql-server)
- [SQL Server Management Studio](https://learn.microsoft.com/ssms/install/install)

1. Склонируйте проект и перейдите в его папку:

   ```powershell
   git clone https://github.com/SUUS123123/FastAPI.git
   cd FastAPI
   ```

2. Создайте виртуальное окружение и установите Python-зависимости:

   ```powershell
   py -3 -m venv .venv
   .\.venv\Scripts\Activate.ps1
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. Создайте локальный файл настроек из шаблона:

   ```powershell
   Copy-Item .env.example .env
   ```

   Проверьте `DB_SERVER` в `.env`. Для стандартного SQL Server Express обычно используется `localhost\SQLEXPRESS`. Если экземпляр сервера имеет другое имя, укажите его. При Windows-аутентификации оставьте `DB_TRUSTED_CONNECTION=yes`.

4. Запустите SQL Server и откройте в SSMS подключение к тому же экземпляру, который указан в `DB_SERVER`. Откройте `create_database.sql` и выполните его. Скрипт создаст пустую базу `ComputerShop`, если её ещё нет. Для создания базы Windows-пользователю нужны соответствующие права.

5. Запустите приложение:

   ```powershell
   .\.venv\Scripts\python.exe -m uvicorn main:app --reload
   ```

   При первом запуске приложение создаст таблицы. Откройте `http://127.0.0.1:8000`; документация API доступна по адресу `http://127.0.0.1:8000/docs`.

Если PowerShell не разрешает активацию окружения, можно пропустить активацию и вызывать `.\.venv\Scripts\python.exe` и `.\.venv\Scripts\pip.exe` напрямую.

## Подключение к базе

`.env.example` содержит безопасный шаблон настроек. Настоящий `.env` не публикуется. При SQL-аутентификации укажите `DB_TRUSTED_CONNECTION=no`, а также `DB_USER` и `DB_PASSWORD`.

Новая база будет пустой. Приложение не загружает демонстрационные товары, участников и покупки. Чтобы перенести текущие данные на другой компьютер, создайте резервную копию базы `ComputerShop` через SSMS (**Tasks → Back Up**), перенесите файл `.bak` отдельно и восстановите его на новом SQL Server (**Databases → Restore Database**). Файл резервной копии не добавляйте в публичный GitHub-репозиторий.

`computer_shop.db` — локальный SQLite-файл старой версии; текущая конфигурация приложения к нему не подключается. Он и другие локальные базы исключены из Git.

## Структура

- `main.py` — создание приложения и инициализация таблиц.
- `app/config.py`, `app/database.py` — настройки и подключение к базе.
- `app/models/` — модели SQLAlchemy.
- `app/schemas/` — Pydantic-схемы запросов и ответов.
- `app/repositories/` — запросы и операции с базой.
- `app/services/` — бизнес-логика.
- `app/api/v1/` — API-маршруты.
- `static/` — веб-интерфейс.
- `create_database.sql` — создание базы данных SQL Server.
