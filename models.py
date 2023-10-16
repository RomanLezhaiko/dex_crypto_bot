import os

from dotenv import load_dotenv
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from db import Base

load_dotenv()

debug = os.getenv('DEBUG')

class Pair(Base):
    __tablename__ = f'pairs_{debug}'

    id = Column(Integer, primary_key=True)
    token_name_1 = Column(String(10))
    token_name_2 = Column(String(10))

    def __repr__(self) -> str:
        return f"<pair {self.id}>"