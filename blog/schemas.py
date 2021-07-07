from typing import Optional
from pydantic.main import BaseModel

class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool]=False


class ShowBlog(BaseModel):
    id: int
    class Config():
        orm_mode= True