from pydantic import BaseModel, Field
from typing import Optional

class ParsedItem(BaseModel):
    id: int
    user_id: int = Field(..., alias="userId")
    title: str
    body: str

    class Config:
        populate_by_name = True