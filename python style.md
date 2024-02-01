## Общие правила и рекомендации:
* Длина строки: не более **120** символов.
* Для проверки формата следует использовать `flake8`
* Для продвинутой проверки типов используйте `mypy`

## Формат строк
Формат кавычек: Для строковых типов следует использовать **двойные** кавычки:

$`\textcolor{green}{\text{Правильно:}}`$
```python
foo = "Это правильный формат строки"
```

$`\textcolor{red}{\text{Неправильно:}}`$
```python
foo = 'Это неправильный формат строки'
```
При переносе строки, следует использовать скобки вместо символа `\`:

$`\textcolor{green}{\text{Правильно:}}`$
```python
foo = (
    "Это начало строки, она очень длинная, поэтому требуется пернести её"
    "а это конец строки, её надо было перенести"
)
```

$`\textcolor{red}{\text{Неправильно:}}`$
```python
foo = "Это начало строки, она очень длинная, поэтому требуется пернести её" \
      "а это конец строки, её надо было перенести"
```



## Документация
Если функция или метод больше трех строк, либо понять, что там написано, сложно при первом приближении. Крайне желательно добавить к ней `docstring`. Формат `docstring`:


$`\textcolor{green}{\text{Правильно:}}`$
```python
def foo(one: str) -> str:
    """Это правильный однострочный докстринг."""
    print(one)
    return one
```

$`\textcolor{red}{\text{Неправильно:}}`$
```python
def foo(one: str) -> str:
    """
    Это не правильный однострочный докстринг
    """
    print(one)
    return one
```
Если при написании `docstring` появилась необходимость переноса на новую строчку:

```python
def foo(one: str) -> str:
    """
    Это правильный многострочный докстринг.
    Это другая строка для докстринга.
    """
    print(one)
    return one
```

## Переносы
При переносе на новую строчку необходимо переносить все элементы:

$`\textcolor{green}{\text{Правильно:}}`$
```python
def foo(one: str) -> str:
    result = add_batch(
            test=1,
            number=None,
            items=items,
            other_items=None,
            bar=1,
        )
    return result
```

$`\textcolor{red}{\text{Неправильно:}}`$
```python
def foo(one: str) -> str:
    result = add_batch(
                test=1, number=None, items=items,
                other_items=None,
                bar=1)
    return result
```

## Импорты
При импортах никогда не следует использовать абсолютный импорт

$`\textcolor{green}{\text{Правильно:}}`$

```python
from foo import bar, another, test
```

$`\textcolor{red}{\text{Неправильно:}}`$

```python
from foo import *
```
Если требуется импортировать множество элементов, следует взять их в скобки и переносить каждый элемент по отдельности:

$`\textcolor{green}{\text{Правильно:}}`$

```python
from foo import (
    one,
    two,
    three,
    four,
    five,
    ...,
)
```

$`\textcolor{red}{\text{Неправильно:}}`$

```python
from foo import one, two, three, \
four, five
```

## Именование переменных, функций и классов

Для переменных следует всегда использовать `snake_case`:

$`\textcolor{green}{\text{Правильно:}}`$
```python
test_variable = "Test"
TEST_CONSTANT = "test"
```

$`\textcolor{red}{\text{Неправильно:}}`$
```python
TestVariable = "Test"
testConstant = "test"
```

Для методов также следует использовать `snake_case`:

$`\textcolor{green}{\text{Правильно:}}`$
```python
def some_function():
    ...
```

$`\textcolor{red}{\text{Неправильно:}}`$
```python
def someFunction():
    ...
```

Для классов необходимо использовать `CamelCase`:

$`\textcolor{green}{\text{Правильно:}}`$
```python
class TetClass:
    ...
```

$`\textcolor{red}{\text{Неправильно:}}`$
```python
class test_class:
    ...
```

## Аннотации типов:
В каждой функции или методе необходимо указывать аннотации типов на входные и выходные данные:
> Исключением являются тесты, там не обязательно указывать аннотации.

$`\textcolor{green}{\text{Правильно:}}`$
```python
def some_function(foo: str, bar: int, test: list[str]) -> dict[str, int]:
    ...
```

$`\textcolor{red}{\text{Неправильно:}}`$
```python
def some_function(foo, bar, test) -> dict[str, int]:
    ...
```

$`\textcolor{red}{\text{Тоже не правильно:}}`$
```python
def some_function(foo: str, bar: int, test: list[str]):
    ...
```
Следует максимально подробно описывать типы при аннотации, но без фанатизма :)

$`\textcolor{green}{\text{Правильно:}}`$
```python
def some_function(foo: str, bar: int, test: list[str]) -> dict[str, int]:
    ...
```

$`\textcolor{red}{\text{Неправильно:}}`$
```python
def some_function(foo: str, bar: int, test: list[str]) -> dict:
    ...
```

## Тесты

### 1. Структура тестов повторяет структуру проекта, для джанго проекта лучше располагать тесты в директориях `django application`.

 `FastApi                                  Django`

![image](uploads/4d7e27c3d9e2d92445f484a98b69accc/image.png)
![image](uploads/b636ced4cd65def59df387f140f44854/image.png)

### 2. Использование Mock + DI предпочтительнее monkeypatch
Monkeypatch стоит применять в end-to-end (допустим тестирование Api endpoint).

Для всех остальных случаев стоит применять `unittest.Mock`

Пример использования `Mock`

```python
@pytest.fixture
def bonus_calculator_mock(db) -> CalculateBonuses:
    # Применение `Mock` в качестве фикстуры
    service = Mock(CalculateBonuses)
    service.calculate.return_value = CalculateBonusesOut(
        mobile_phone="79249242367",
        accrual_amount=15,
        max_payment_amount=1,
        expiration=datetime.datetime.now(),
    )

    return service


class TestAcceptOrders:

    async def test_incorrect_bonus_payment_failure(self, db, outlets_repo, bonus_calculator_mock):
        assert not await db.orders.count_documents({})
        items = OrderItemFactory.batch(3, price=100, quantity=1)
        orders = OrderFactory.batch(3, items=items, number=None, delivery_date=None, bonus_payment=200)
        outlets = [OutletFactory.build(id=o.pickup_location_id) for o in orders]
        await outlets_repo.add_many(outlets)

        # Если необходимо переопределить `Mock` для конкретного тест кейса.
        raises_validator = Mock(BonusesPaymentValidator)
        raises_validator.validate.side_effect = OrderConstraintError()

        with pytest.raises(OrderConstraintError):
            await AcceptOrders(
                db=db,
                orders=orders,
                bonus_calculator=bonus_calculator_mock,
                bonus_validator=raises_validator,
            ).execute()


```

Обсуждение на тему когда необходимо использовать `monkeypatch`, а когда `Mock` по [ссылке](https://github.com/pytest-dev/pytest/issues/4576)

### 4. Для каждого метода желательно отдельный класс и в нём уже список тестов.

```python
class TestCategoriesRepositoryAddMany:
    async def test_add_many_success(
        self,
        category_repo,
        category_collection,
    ):
        ...

    @pytest.mark.parametrize("name, exp_slug", (("Some Name", "some-name"), ("Витамины и БАДы", "vitaminy-i-bady")))
    async def test_when_category_created_then_slug_autogenerated(
        self,
        category_repo,
        category_collection,
        name,
        exp_slug,
    ):
        ...


class TestCategoriesRepositoryGetFiltered:
    @pytest.mark.parametrize(
        "count",
        (0, 4, 13),
    )
    async def test_when_parent_not_set_in_filter_then_query_not_filtered_by_parent(
        self,
        category_repo,
        count,
    ):
       ...

    async def test_when_parent_is_str_null_then_only_root_categories_in_result(
        self,
        category_repo,
    ):
        ...

    async def test_when_parent_is_set_then_only_with_this_parent_categories_in_result(
        self,
        category_repo,
    ):
        ...
```

### 5. Необходимо стараться использовать нижеприведенные паттерны при наименовании тест кейсов.

- `test_when_<тестируемое условие>_then_<ожидаемый результат>`

  - Пример:

    ```python
    def test_when_items_contain_special_characters_then_this_remove_from_group_title():
        ...

    def test_when_invalid_promocode_then_order_canceled():
        ...
    ```

- `test_<тестируемый функционал>_<ожидаемый результат>`

  - Пример:

    ```python
    def test_get_user_success():
        ...

    def test_get_user_raise_value_error():
        ...
    ```
