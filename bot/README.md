## бот который являеться фронтендом
создайте в bot/ файл run.sh и запишите туда следуйщий код:
```
export token=токен бота
export api_address=http://127.0.0.1:8000/

python main.py
```

и запустите скрипт командой source run.sh не забывая что нужно ещё активировать virtualenv на poetry
