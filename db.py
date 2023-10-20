import os

from sqlalchemy import MetaData
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base

# basedir = os.path.abspath(os.path.dirname(__file__))

# SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(basedir, 'storage.db')}?check_same_thread=False"

# engine = create_engine(SQLALCHEMY_DATABASE_URI, connect_args={'timeout': 25})
# engine = create_engine(SQLALCHEMY_DATABASE_URI)
# engine = create_engine("postgresql+psycopg2://root:pass@localhost/mydb")
engine = create_engine("postgresql+psycopg2://postgres:postgres_password@db:5432/postgres")
# engine = create_engine('postgresql://user:user_password@{}:5432/database'.format('service_name_of_postgres'))


Session = scoped_session(
    sessionmaker(autocommit=False,
                 autoflush=False,
                 bind=engine))
Base = declarative_base()
Base.query = Session.query_property()
