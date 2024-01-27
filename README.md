# Y_LAB Task 1

### *__Y_LAB TASK 1__* is a task for company Y_LAB university. The main assignment was to create an FastAPI app performing Restaurant service.

### Conditions:

В этом домашнем задании надо написать тесты для ранее разработанных ендпоинтов вашего API после Вебинара №1.

Обернуть программные компоненты в контейнеры. Контейнеры должны запускаться по одной команде “docker-compose up -d” или той которая описана вами в readme.md.

Образы для Docker:
(API) python:3.10-slim
(DB) postgres:15.1-alpine

1. Написать CRUD тесты для ранее разработанного API с помощью библиотеки pytest
2. Подготовить отдельный контейнер для запуска тестов. Команду для запуска указать в README.md
3. ** Реализовать вывод количества подменю и блюд для Меню через один (сложный) ORM запрос.
4. *** Реализовать тестовый сценарий «Проверка кол-ва блюд и подменю в меню» из Postman с помощью pytest.

Если FastAPI синхронное - тесты синхронные, Если асинхронное - тесты асинхронные


**Оборачиваем приложение в докер.

***CRUD – create/update/retrieve/delete.
1. Firstly, you need to add venv file by this command:
   ```python 
    python -m venv venv
2. Create a ".env" file at the root of the directory with params:
   ```python
   ALL SETTINGS FOR POSTGRESQL
   
   DB_NAME=postgres
   DB_USER=postgres
   DB_PASS=postgres
   DB_HOST=db
   DB_PORT=5432
   
   POSTGRES_DB=postgres
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=postgres
   
   DB_NAME_TEST=testdb
   DB_USER_TEST=postgres
   DB_PASS_TEST=postgres
   DB_HOST_TEST=testdb
   DB_PORT_TEST=5432
3. Start docker-compose.yaml by the command:
   ```python
   docker compose up -d --build

