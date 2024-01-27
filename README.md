# Y_LAB Task 1

### *__Y_LAB TASK 1__* is a task for company Y_LAB university. The main assignment was to create an FastAPI app performing Restaurant service.

### Conditions:

Написать проект на FastAPI с использованием PostgreSQL в качестве БД. В проекте следует реализовать REST API по работе с
меню ресторана, все CRUD операции. Для проверки задания, к презентаций будет приложена Postman коллекция с тестами.
Задание выполнено, если все тесты проходят успешно.
Даны 3 сущности: Меню, Подменю, Блюдо.

Зависимости:

- У меню есть подменю, которые к ней привязаны.
- У подменю есть блюда.

Условия:

- Блюдо не может быть привязано напрямую к меню, минуя подменю.
- Блюдо не может находиться в 2-х подменю одновременно.
- Подменю не может находиться в 2-х меню одновременно.
- Если удалить меню, должны удалиться все подменю и блюда этого меню.
- Если удалить подменю, должны удалиться все блюда этого подменю.
- Цены блюд выводить с округлением до 2 знаков после запятой.
- Во время выдачи списка меню, для каждого меню добавлять кол-во подменю и блюд в этом меню.
- Во время выдачи списка подменю, для каждого подменю добавлять кол-во блюд в этом подменю.
- Во время запуска тестового сценария БД должна быть пуста.

1. Firstly, you need to add venv file by this command:
   ```python 
    python -m venv venv
2. Install dependencies:
   ```python
   poetry install
3. Create a ".env" file at the root of the directory with params:
   ```python
   ALL SETTINGS FOR POSTGRESQL
   
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
4. Start an app from core.py file:
### core.py
> ![photo](https://i.imgur.com/Gorj4Pi.png)

