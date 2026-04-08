from pydantic import BaseModel

class Game(BaseModel):
    name: str
    link: str
    