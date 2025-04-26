from pydantic import BaseModel
from typing import List,Optional


class Blog(BaseModel):
    title : str
    content : str

    class Config:
        from_attributes : True
