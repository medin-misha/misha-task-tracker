# Привет ✌️  
Это Telegram-бот, который поможет тебе планировать задачи, чтобы ты наконец поднял свою ж**у с дивана. Он умеет:  
- Создавать/удалять задачи  
- Считать, сколько раз ты выполнил ту или иную задачу  
- Выдавать график на N дней вперёд  
- Показывать все/выполненные/невыполненные задачи  

Весь этот функционал доступен в Telegram-боте.  

### Как запустить?
Запуск происходит достаточно просто. Разберём поэтапно:  

1. **Создать файлы:**  
    - `backend/app/run.sh`  
      В нём пропиши:  
      ```bash
      #!/bin/bash
      export POSTGRES_HOST=postgres/postgres_db
      export POSTGRES_USER=postgres_user
      export POSTGRES_PASSWORD=postgres_password

      poetry run alembic revision --autogenerate -m "migration"
      poetry run alembic upgrade head
      poetry run gunicorn main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:80
      ```  
      - `bot/run.sh`
      В нём пропиши: 
      ```bash
      #!/bin/bash

      export TOKEN=токен_бота
      export API_ADDRESS=http://127.0.0.1:8000/
      python main.py
      ```  

    **Примечание:**  
    Переменные окружения (`export`) должны быть направлены на твою PostgreSQL-базу данных. По умолчанию мой шаблон удовлетворяет этому требованию.  

2. Запустить бэкенд:  
   ```bash
   docker-compose up --build
   ```  

3. Перейти в `./bot`, создать виртуальное окружение и установить Poetry:  
   ```bash
   pip install poetry
   poetry install
   ```  

4. Запустить бота:  
   ```bash
   source run.sh
   ```  

Готово 🎉 Удачи в достигаторстве.

 
