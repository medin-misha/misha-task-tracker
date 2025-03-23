# Бэкенд 💫  
Это приложение на **FastAPI** + **SQLAlchemy** + **Alembic**. В качестве менеджера пакетов используется **Poetry**. Бэкенд подключён к **PostgreSQL** и служит API для Telegram-бота (который находится в этом же репозитории).  

## Где, как и что? 🧐  
Папка `app/` содержит само приложение. Внутри неё находятся:  
- **`run.sh`** — скрипт, который устанавливает переменные окружения (по умолчанию они работают).  
- **`main.py`** — главный файл приложения, в котором подключаются все роутеры к FastAPI.  
- **`alembic.ini`** — конфигурационный файл Alembic.  
- **`alembic/`** — файлы и миграции Alembic.  
- **`handlers/`** — обработчики запросов.  
- **`core/`** — модели, конфигурация, вспомогательные функции для работы с базой данных, аутентификация и шаблонизатор планирования задач.  

## Запуск ↗︎  
Запуск происходит из корневой директории (там, где папки `backend/` и `bot/`).  

1. Создайте файл `backend/app/run.sh` и добавьте в него следующий код:  

   ```bash
   #!/bin/bash
   export POSTGRES_HOST=postgres/postgres_db
   export POSTGRES_USER=postgres_user
   export POSTGRES_PASSWORD=postgres_password

   poetry run alembic revision --autogenerate -m "migration"
   poetry run alembic upgrade head
   poetry run gunicorn main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:80
   ```  

2. В корневой директории запустите команду:  

   ```bash
   docker-compose up --build
   ```  

Готово! Теперь просто открой `127.0.0.1:8000/docs` — там ты найдёшь всю документацию API. 🚀  
