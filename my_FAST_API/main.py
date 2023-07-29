# Импортируем класс FastAPI из модуля fastapi
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from models import User, external_data, Feedback

# Создаем экземпляр класса FastAPI, который будет представлять наше приложение
app = FastAPI()


# Определяем обработчик (handler) для HTTP GET запроса на корневой URL "/".
# Обработчик будет асинхронной функцией, так как FastAPI поддерживает асинхронные запросы.
# В данном случае, обработчик просто возвращает JSON-объект с сообщением "Hello World".
@app.get("/")
async def root():
    # Возвращаем словарь, который автоматически будет преобразован в JSON-ответ сервера
    return {"message": "Hello World"}


@app.get('/custom')
async def read_custom_message():
    return {"message": 'My custom message'}


# Определяем обработчик GET-запроса для маршрута "/2.2"
@app.get('/2.2')
def show_name_id():
    # Создаем экземпляр модели User, передавая ему данные из external_data
    user = User(**external_data)
    # Возвращаем данные о пользователе в формате JSON
    return user


"""Ваша задача состоит в том, чтобы расширить существующее приложение FastAPI, добавив новую конечную точку POST, 
которая принимает данные JSON, представляющие пользователя, и возвращает те же данные с дополнительным полем, 
указывающим, является ли пользователь взрослым или нет.

1. Определите Pydantic модель с именем "Пользователь" ("User") со следующими полями:

   - `name` (str)

   - `age` (int)

2. Создайте новый маршрут `/user`, который принимает запросы POST и принимает полезную нагрузку JSON, содержащую 
пользовательские данные, соответствующие модели `User`.

3. Реализуйте функцию для проверки того, является ли пользователь взрослым (возраст >= 18) или несовершеннолетним (
возраст < 18).

4. Верните пользовательские данные вместе с дополнительным полем `is_adult` в ответе JSON, указывающим, является ли 
пользователь взрослым (True) или несовершеннолетним (False).


"""


# Определяем маршрут для обработки POST-запроса на /user
@app.post('/user')
async def check_adult_status(user: User):
    # Проверяем, является ли пользователь взрослым (старше 18 лет)
    is_adult = user.age >= 18

    # Преобразуем объект user в словарь с помощью метода model_dump()
    user_dict = user.model_dump()

    # Добавляем поле 'is_adult' со значением True или False в зависимости от статуса взрослости
    user_dict['is_adult'] = is_adult

    # Возвращаем ответ в формате JSON с данными пользователя и полем is_adult
    return user_dict


# Создаем экземпляр FastAPI для второго приложения
app_2 = FastAPI()


# Обработчик для отображения страницы index.html
@app_2.get('/', response_class=HTMLResponse)
async def root_2():
    # Открываем файл index.html в режиме чтения (r)
    with open('index.html', 'r') as file:
        # Читаем содержимое файла и сохраняем в переменную content
        content = file.read()
        # Возвращаем HTMLResponse с содержимым страницы index.html
        return HTMLResponse(content=content)


app_23 = FastAPI()

# Пример пользовательских данных (для демонстрационный целей)
fake_users = {
    1: {"username": "john_doe", "email": "john@example.com"},
    2: {"username": "jane_smith", "email": "jane@example.com"},
}


# Конечная точка для получения информации о пользователе по ID
@app_23.get("/users/{user_id}")
def read_user(user_id: int):
    if user_id in fake_users:
        return fake_users[user_id]
    return {"error": "User not found"}


app_23_lim = FastAPI()

# Пример пользовательских данных (для демонстрационный целей)
fake_users_lim = {
    1: {"username": "john_doe", "email": "john@example.com"},
    2: {"username": "jane_smith", "email": "jane@example.com"},
    3: {"username": "alice", "email": "alice@example.com"},
    4: {"username": "bob", "email": "bob@example.com"},
    5: {"username": "emily", "email": "emily@example.com"},
    6: {"username": "alex", "email": "alex@example.com"},
    7: {"username": "sophia", "email": "sophia@example.com"},
    8: {"username": "michael", "email": "michael@example.com"},
    9: {"username": "olivia", "email": "olivia@example.com"},
    10: {"username": "william", "email": "william@example.com"},
}


# Конечная точка для получения информации о пользователе по ID
@app_23_lim.get("/users/")
def read_user(limit: int = 10):
    return dict(list(fake_users_lim.items())[:limit])


"""Расширьте существующее приложение FastAPI, создав конечную точку POST, которая позволяет пользователям отправлять 
отзывы. Конечная точка должна принимать данные JSON, содержащие имя пользователя и сообщение обратной связи.
Создайте новый маршрут публикации "/feedback", который принимает данные JSON в соответствии с моделью `Feedback`.
"""

app_feadbeack = FastAPI()
# Хранилище данных для сохранения обратной связи
feedback_data = []


# Обработчик POST-запроса на маршрут "/feedback/"
@app_feadbeack.post("/feedback")
async def come_in_feadbeack(feedback: Feedback):
    # Добавляем данные обратной связи в хранилище
    feedback_data.append(feedback.model_dump())
    # Формируем ответное сообщение
    response_message = f"Feedback received. Thank you, {feedback.name}!"
    # Возвращаем ответ в формате JSON
    return {'message': response_message}
