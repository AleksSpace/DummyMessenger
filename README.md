# DummyMessenger

# Стек:
 - python 3.10
 - FastAPI
 - Postgresql
 - SQLAlchemy
 - httpx
 - uvicorn

# Установка:

Клонируйте репозиторий к себе на компьютер:  

```
git clone https://github.com/AleksSpace/DummyMessenger.git
```

# Запуск:
Запуск в Docker:
- перейдите в директорию приложения
- в корневой папке (там где находится файл docker-compose.yml), в терминале, выполните команду ``` docker compose -f "docker-compose.yml" up -d --build ```  
Соберутся Docker контейнеры и начнут отправляться запросы.  
Результат работы вы можете увидеть в приложении Docker Desktop, или через терминал, введя команду:
``` docker logs -f dummymessenger-client-1 ```.  
Чтобы проверить, что нет дубликатов, воспользуйтесь приложением PgAdmin, например, или подключитесь к БД через терминал.  
Для проверки введите команду:
```
SELECT sender, user_message_count, COUNT(*)
FROM messages
GROUP BY sender, user_message_count
HAVING COUNT(*) > 1;
```
Если вернется пустой ответ, значит дубликатов нет.

Чтобы проверить ответ от одного запроса, перейдите по адресу ` http://127.0.0.1:80/docs `  
и сделайте запрос через интерактивную документацию.

В ответ вернётся:
```
[
  {
    "id": 0,                                     - порядковый номер сообщения
    "sender": "string",                          - Имя отправителя
    "text": "string",                            - Текст сообщения
    "created_at": "2023-10-04T09:56:58.084Z",    - Время отправки сообщения
    "user_message_count": 0                      - Кол-во сообщений отправленных этим отправителем
  }
]
```
