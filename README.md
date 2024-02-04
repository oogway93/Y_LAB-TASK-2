# Y_LAB Task 2

### *__Y_LAB TASK 2__* is a task for company Y_LAB university. The main assignment was to create an FastAPI app performing Restaurant service.

### Conditions:

В этом домашнем задании надо написать тесты для ранее разработанных ендпоинтов вашего API после Вебинара №1.

Обернуть программные компоненты в контейнеры. Контейнеры должны запускаться по одной команде “docker-compose up -d” или
той которая описана вами в readme.md.

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

### __Ответ на 3 пункт в db/queries.py с 42 строчки.__

# TASK 3
1.Вынести бизнес логику и запросы в БД в отдельные слои приложения.

2.Добавить кэширование запросов к API с использованием Redis. Не забыть про инвалидацию кэша.

3.Добавить pre-commit хуки в проект. Файл yaml будет прикреплен к ДЗ.

4.Покрыть проект type hints (тайпхинтами)

5.* Описать ручки API в соответствий c OpenAPI

6.** Реализовать в тестах аналог Django reverse() для FastAPI

Требования:
1. Код должен проходить все линтеры.
2. Код должен соответствовать принципам SOLID, DRY, KISS.
3. Проект должен запускаться по одной команде (докер).
4. Проект должен проходить все Postman тесты (коллекция с Вебинара №1).
5. Тесты написанные вами после Вебинара №2, должны быть актуальны, запускать и успешно проходить

Дополнительно:
Контейнеры с проектом и с тестами запускаются разными командами.

1. Firstly, you need to add venv file by this command:
   ```python
    python -m venv venv
2. Create a ".env" file at the root of the directory with params:
   ```python
   DB_NAME=postgres
   DB_USER=postgres
   DB_PASS=postgres
   DB_HOST=db
   DB_PORT=5432

   DB_NAME_TEST=testdb
   DB_USER_TEST=postgres
   DB_PASS_TEST=postgres
   DB_HOST_TEST=testdb
   DB_PORT_TEST=5432

   REDIS_HOST=redis
3. Start docker-compose.test.yaml by the command:
      ```python
   docker compose -f docker-compose.test.yaml up -d --build
4. Start docker-compose.prod.yaml by the command:
   ```
   docker compose -f docker-compose.prod.yaml up -d --build
