# Приложение ИИ-ассистент инженера по гарантии

## Структура проекта:

<ol>
  <li>Реализация векторной базы данных ChromaDB</li>
  <li>Реализация регистрации и авторизации</li>
  <li>Создание веб-чата с выбором нейросети DeepSeek | Mistral</li>
  <li>Интеграция через FastAPI</li>
  <li>Интеграция админ-панели с помощью fastadmin</li>
  <li>Сборка проекта в Docker compose</li>
</ol>

## Приложение

<img src="media/registration.png" width="400" height: auto>
<img src="media/login.png" width="400" height: auto>
<img src="media/assistant.png" width="400" height: auto>
<img src="media/admin.png" width="400" height: auto>

## Развертывание

Для развертывания проекта используйте Docker. Убедитесь, что у вас установлены Docker и Docker Compose. Выполните следующие команды:

```
docker compose up --build
docker compose exec app alembic revision --autogenerate -m "Initial revision"
docker compose exec app alembic upgrade head
```
После успешного выполнения этих команд приложение будет доступно по адресу:
<http://127.0.0.1:8000/auth/login/>

Админ панель будет доступна по адресу:
<http://127.0.0.1:8000/admin/>

Для создания базы данных ChromaDB воспользуйтесь скриптами из: app/database_utils


## Стек технологий

![FastAPI](https://img.shields.io/badge/FastAPI-009639?style=flat
)
![ChromaDB](https://img.shields.io/badge/ChromaDB-111111?style=flat
)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)