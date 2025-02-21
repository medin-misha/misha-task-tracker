### таск трекер
Это таск трекер который будет.
### как запустить
Запуск происходит достаточно просто. разберём поэтапно:
1. файлы которые нужно создать
    1. `touch backend/app/run.sh` там пропиши:
       ```
        #!/bin/bash
        export postgres_host=postgres/postgres_db
        export postgres_user=postgres_user 
        export postgres_password=postgres_password
        
        poetry run alembic upgrade head
        poetry run gunicorn main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:80    %                                                        
       ``` 
    export-ы это переменные окружения. Учти что они должны быть направленны на твою postgres базу данных. (по умолчанию мой шаблон удовлетворяет этому требованию)
2. `docker-compose up --build` запуск
