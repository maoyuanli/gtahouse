import os

from sqlalchemy import create_engine, Column, Integer, TEXT
from sqlalchemy.ext.declarative import declarative_base

database_name = 'datalake.db'
cur_path = os.path.dirname(__file__)
par_path = os.path.dirname(cur_path)
database_file = os.path.join(os.path.abspath(par_path), database_name)
db_url = 'sqlite:///{0}'.format(database_file)
conn = create_engine(db_url)
Base = declarative_base(bind=conn)


# database table model
class Tweet(Base):
    __tablename__ = 'tweets'
    id = Column(Integer, nullable=False, primary_key=True)
    author = Column(TEXT, nullable=False)
    tweet = Column(TEXT, nullable=False)
    timestamp = Column(TEXT, nullable=False)


# sqlite database file utility class
class DatabaseUtil:
    tweet = Tweet()

    def init_db(self):
        if not os.path.isfile(database_file):
            Base.metadata.create_all()

    def get_engine(self):
        engine = create_engine(db_url)
        return engine

# initialize/create datalake.db
tdb = DatabaseUtil()
tdb.init_db()
