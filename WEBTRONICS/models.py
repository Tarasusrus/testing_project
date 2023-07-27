from pydantic import BaseModel


class Post(BaseModel):
    id: int
    title: str
    content: str


class Like(BaseModel):
    user_id: int
    post_id: int


class Dislike(BaseModel):
    user_id: int
    post_id: int
