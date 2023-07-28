from fastapi import FastAPI, HTTPException
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi

from auth import create_access_token
from models import Post, Like, Dislike

app = FastAPI()
users_db = [
    {"username": "user1", "password": "password1"},
    {"username": "user2", "password": "password2"},
]

posts_db = [
    {"id": 1, "title": "Post 1", "content": "Content 1"},
    {"id": 2, "title": "Post 2", "content": "Content 2"},
]

post_likes_cache = {}
post_dislikes_cache = {}


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    """
    Возвращает HTML-страницу с пользовательским интерфейсом Swagger UI.

    Returns:
        str: HTML-страница с интерфейсом Swagger UI.
    """
    return get_swagger_ui_html(openapi_url="/openapi.json", title="Custom Swagger UI")


@app.get("/openapi.json", include_in_schema=False)
async def get_open_api_endpoint():
    """
    Возвращает JSON-схему OpenAPI для текущего приложения FastAPI.

    Returns:
        dict: JSON-схема OpenAPI для текущего приложения.
    """
    return get_openapi(
        title="Custom OpenAPI",
        version="1.0.0",
        routes=app.routes,
    )


@app.post("/register")
async def register_user(username: str, password: str):
    """
    Регистрирует нового пользователя с заданным именем и паролем.

    Args:
        username (str): Имя пользователя.
        password (str): Пароль пользователя.

    Returns:
        dict: Словарь с сообщением об успешной регистрации.

    Raises:
        HTTPException: Если пользователь с таким именем уже существует (код 400).
    """
    # Проверяем, что пользователь с таким именем не существует
    for user in users_db:
        if user["username"] == username:
            raise HTTPException(status_code=400, detail="User already exists")

    # Создаем нового пользователя
    new_user = {"username": username, "password": password}
    users_db.append(new_user)

    return {"message": "User registered successfully"}


@app.post("/login")
async def login(username: str, password: str):
    """
    Аутентифицирует пользователя по заданному имени и паролю и возвращает JWT токен.

    Args:
        username (str): Имя пользователя.
        password (str): Пароль пользователя.

    Returns:
        dict: Словарь с JWT токеном в случае успешной аутентификации.

    Raises:
        HTTPException: Если заданные учетные данные недействительны (код 401).
    """
    # Ищем пользователя в "базе данных"
    for user in users_db:
        if user["username"] == username and user["password"] == password:
            # Генерируем JWT токен и отправляем его в ответе
            token = create_access_token({"sub": username})
            return {"access_token": token}

    raise HTTPException(status_code=401, detail="Invalid credentials")


@app.post("/posts/", response_model=Post)
async def create_post(post: Post):
    """
    Создает новый пост и добавляет его в базу данных.

    Args:
        post (Post): Модель данных для нового поста.

    Returns:
        model_dump: Словарь с данными нового поста, включая сгенерированный уникальный ID.

    Raises:
        HTTPException: Если не удалось создать пост или произошла ошибка при добавлении в базу данных.
    """
    # Генерируем уникальный ID для нового поста
    new_post_id = max(post.id for post in posts_db) + 1 if posts_db else 1
    post_data = post.model_dump()
    post_data["id"] = new_post_id

    # Добавляем новый пост в "базу данных"
    posts_db.append(post_data)
    return post_data


@app.get("/posts/{post_id}", response_model=Post)
async def read_post(post_id: int):
    """
    Возвращает данные о посте с указанным ID.

    Args:
        post_id (int): Идентификатор поста, который нужно найти.

    Returns:
        dict: Словарь с данными о посте, если он найден.

    Raises:
        HTTPException: Если пост с указанным ID не найден (ошибка 404).
    """
    # Ищем пост с указанным ID в "базе данных"
    for post in posts_db:
        if post["id"] == post_id:
            return post

    raise HTTPException(status_code=404, detail="Post not found")


@app.put("/posts/{post_id}", response_model=Post)
async def update_post(post_id: int, post: Post):
    """
    Обновляет данные о посте с указанным ID.

    Args:
        post_id (int): Идентификатор поста, который нужно обновить.
        post (Post): Модель данных Post с новыми данными для обновления.

    Returns:
        dict: Словарь с обновленными данными о посте, если он найден.

    Raises:
        HTTPException: Если пост с указанным ID не найден (ошибка 404).
    """
    # Ищем пост с указанным ID в "базе данных"
    for i, p in enumerate(posts_db):
        if p["id"] == post_id:
            # Обновляем данные поста
            posts_db[i] = post.model_dump()
            return posts_db[i]

    raise HTTPException(status_code=404, detail="Post not found")


@app.delete("/posts/{post_id}", response_model=Post)
async def delete_post(post_id: int):
    """
    Удаляет пост с указанным ID из "базы данных".

    Args:
        post_id (int): Идентификатор поста, который нужно удалить.

    Returns:
        dict: Словарь с данными об удаленном посте, если он найден.

    Raises:
        HTTPException: Если пост с указанным ID не найден (ошибка 404).
    """
    # Ищем пост с указанным ID в "базе данных" и удаляем его
    for i, post in enumerate(posts_db):
        if post["id"] == post_id:
            deleted_post = posts_db.pop(i)
            return deleted_post

    raise HTTPException(status_code=404, detail="Post not found")


@app.post("/posts/{post_id}/like/", response_model=Like)
async def like_post(post_id: int, like: Like):
    """
    Ставит лайк на пост с указанным ID и сохраняет лайк в кэше.

    Args:
        post_id (int): Идентификатор поста, на который нужно поставить лайк.
        like (Like): Модель данных Like, содержащая информацию о лайке (например, ID пользователя).

    Returns:
        dict: Словарь с данными о поставленном лайке.

    Raises:
        HTTPException: Если пользователь пытается поставить лайк своему собственному посту (ошибка 400).
    """
    # Проверяем, что пользователь не ставит лайк своему посту
    for post in posts_db:
        if post["id"] == post_id and post["user_id"] == like.user_id:
            raise HTTPException(status_code=400, detail="You cannot like your own post")

        # Проверяем, что пост с указанным post_id существует
    if not any(post["id"] == post_id for post in posts_db):
        raise HTTPException(status_code=404, detail="Post not found")

    like_data = like.model_dump()
    like_data["post_id"] = post_id

    # Добавляем лайк в кэш
    if post_id not in post_likes_cache:
        post_likes_cache[post_id] = []
    post_likes_cache[post_id].append(like_data)

    return like_data


@app.post("/posts/{post_id}/dislike/", response_model=Dislike)
async def dislike_post(post_id: int, dislike: Dislike):
    """
    Ставит дизлайк на пост с указанным ID и сохраняет дизлайк в кэше.

    Args:
        post_id (int): Идентификатор поста, на который нужно поставить дизлайк.
        dislike (Dislike): Модель данных Dislike, содержащая информацию о дизлайке (например, ID пользователя).

    Returns:
        dict: Словарь с данными о поставленном дизлайке.

    Raises:
        HTTPException: Если пользователь пытается поставить дизлайк своему собственному посту (ошибка 400).
    """
    # Проверяем, что пользователь не ставит дизлайк своему посту
    for post in posts_db:
        if post["id"] == post_id and post["user_id"] == dislike.user_id:
            raise HTTPException(status_code=400, detail="You cannot dislike your own post")

    dislike_data = dislike.model_dump()
    dislike_data["post_id"] = post_id

    # Добавляем дизлайк в кэш
    if post_id not in post_dislikes_cache:
        post_dislikes_cache[post_id] = []
    post_dislikes_cache[post_id].append(dislike_data)

    return dislike_data


@app.get("/posts/{post_id}", response_model=Post)
async def read_post(post_id: int):
    """
    Возвращает информацию о посте с указанным ID, включая количество лайков и дизлайков из кэша.

    Args:
        post_id (int): Идентификатор поста, информацию о котором нужно получить.

    Returns:
        dict: Словарь с данными о посте, включая количество лайков и дизлайков.

    Raises:
        HTTPException: Если пост с указанным ID не найден (ошибка 404).
    """
    # Ищем пост с указанным ID в "базе данных"
    for post in posts_db:
        if post["id"] == post_id:
            # Получаем количество лайков и дизлайков из кэша
            like_count = len(post_likes_cache.get(post_id, set()))
            dislike_count = len(post_dislikes_cache.get(post_id, set()))

            # Добавляем информацию о количестве лайков и дизлайков в ответ
            post["like_count"] = like_count
            post["dislike_count"] = dislike_count

            return post

    raise HTTPException(status_code=404, detail="Post not found")
