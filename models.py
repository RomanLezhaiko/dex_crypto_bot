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
    pair_address = Column(String(50))
    pair_abi = Column(String(3000))
    pair_number = Column(Integer)

    profile = relationship('Token', backref='pairs', uselist=False)


    def __repr__(self) -> str:
        return f"<pair {self.id}>"


class Token(Base):
    __tablename__ = f'token_{debug}'

    id = Column(Integer, primary_key=True)
    token_name = Column(String(20))
    token_address = Column(String(50))
    token_position = Column(Integer)
    
    pair_id = Column(Integer, ForeignKey(f'pairs_{debug}.id'))