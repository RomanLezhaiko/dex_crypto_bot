import os

from dotenv import load_dotenv
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from models import Pair
from db import Base, engine

# load_dotenv()
# debug = os.getenv('DEBUG')


def init_db():
    # # Устанавливаем соединение с postgres
    # connection = psycopg2.connect(user="postgres", password="postgres")
    # connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    # # Создаем курсор для выполнения операций с базой данных
    # cursor = connection.cursor() 
    # # Создаем базу данных
    # cursor.execute('create database sqlalchemy_tuts')
    # # Закрываем соединение
    # cursor.close()
    # connection.close()

    Base.metadata.create_all(bind=engine)
    print("Initialized the db")


if __name__ == "__main__":
    init_db()