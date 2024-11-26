# Task Tracker API

## Описание:
Это API создания и отслеживания проектов с удобным функционалом. 
Здесь используются такие технологии как DjangoRestFramework, WebSocket, PostgreSQL, JWT. 
Все они позволяют сделать работы с данных API максимально функциональной и удобной.

## Инструкция по запуску:
Пропишите следующие команды в консоль:
```python
git clone https://github.com/criger52/TaskTracker.git
cd .\TaskTrackerformgit\
docker-compose build
docker-compose up -d
```
Что бы остановить:
```python
docker-compose down
```

При повторном запуске будет достаточно лишь:
```python
docker-compose up -d
```
Теперь вы можете получить доступ к вашему приложению 
в браузере по адресу: http://localhost:8000

Если вы хотите создать супер пользователя, то вам необходимо после того как 
вы прописали ```docker-compose up -d```, пропишите следующую команду:
```
docker-compose exec web python manage.py createsuperuser
```
