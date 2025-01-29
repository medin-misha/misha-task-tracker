### таск трекер
Это таск трекер который будет.
### как запустить
Запуск происходит достаточно просто. разберём поэтапно:
1. ./ `docker-compose up --build` - запуск базы данных.
    PostgreSQL бд с базовыми логином и паролем.
    - POSTGRES_USER: postgres_user
    - POSTGRES_PASSWORD: postgres_password
    - POSTGRES_DB: postgres_db
    в проекте данные типа логина и пароля находяться по пути backend/core/config.py
2. ./backend/ `touch setenv.sh` - это исполняемый файл который будет ставить переменные окружения. Вот его шаблон:
    ```sh
    export postgres_host=localhost/postgres_db
    export postgres_user=postgres_user
    export postgres_password=postgres_password
    ```
3. ./backend/ `openssl genrsa -out keys/private.pem 2048`, `openssl rsa -in keys/private.pem -outform PEM -pubout -out keys/public.pem` (не обязательно)
    это создание приватного и публичного улюча (на основе приватного) (добавил по невнимательности, может что то придумаю с этим)
. ./ `python -m venv venv`, `source venv/bin/activate` | `venv/Scripts/activate`, `poetry install`, `cd backend`, `uvicorn main:app --reload` 
