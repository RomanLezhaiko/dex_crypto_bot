import os

from sqlalchemy import MetaData
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(basedir, 'storage.db')}?check_same_thread=False"

engine = create_engine(SQLALCHEMY_DATABASE_URI)
# sql_meta = MetaData(engine)
Session = scoped_session(
    sessionmaker(autocommit=False,
                 autoflush=False,
                 bind=engine))
Base = declarative_base()
Base.query = Session.query_property()

# def init_db():
#     import models
#     # sql_meta.create_all()
#     Base.metadata.create_all(bind=engine)
#     print('All good')


# if __name__ == "__main__": 
#     init_db()