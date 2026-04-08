# models/game.py
from sqlalchemy import Column, Integer, String
from repository.database import Base

class Game(Base):
    __tablename__ = 'games'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    link = Column(String, nullable=False)
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "link": self.link
        }
    
    def __repr__(self):
        return f"<Game(id={self.id}, name='{self.name}', link='{self.link}')>"