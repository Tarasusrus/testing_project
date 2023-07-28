from pydantic import BaseModel


class Post(BaseModel):
    """
    Модель данных для поста (Post).

    Attributes:
        id (int): Идентификатор поста.
        title (str): Заголовок поста.
        content (str): Содержание поста.
    """
    id: int
    title: str
    content: str


class Like(BaseModel):
    """
    Модель данных для лайка (Like).

    Attributes:
        user_id (int): Идентификатор пользователя, который поставил лайк.
        post_id (int): Идентификатор поста, которому был поставлен лайк.
    """
    user_id: int
    post_id: int


class Dislike(BaseModel):
    """
    Модель данных для дизлайка (Dislike).

    Attributes:
        user_id (int): Идентификатор пользователя, который поставил дизлайк.
        post_id (int): Идентификатор поста, которому был поставлен дизлайк.
    """
    user_id: int
    post_id: int
