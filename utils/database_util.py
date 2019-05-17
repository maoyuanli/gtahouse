import os

from sqlalchemy import create_engine, Column, Integer, TEXT, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

database_name = 'datalake.db'
cur_path = os.path.dirname(__file__)
par_path = os.path.dirname(cur_path)
database_file = os.path.join(os.path.abspath(par_path), database_name)
db_url = 'sqlite:///{0}'.format(database_file)
conn = create_engine(db_url)
Base = declarative_base(bind=conn)


# database table model
class Tweets(Base):
    __tablename__ = 'tweets'
    id = Column(Integer, primary_key=True, nullable=False)
    author = Column(TEXT, nullable=False)
    tweet = Column(TEXT, nullable=False)
    time = Column(TEXT, nullable=False)
    type = Column(String(200), nullable=False)


# sqlite database file utility class
class DatabaseUtil:
    # tweet = Tweet()

    def init_db(self):
        if not os.path.isfile(database_file):
            Base.metadata.create_all()

    def get_engine(self):
        engine = create_engine(db_url)
        return engine

    def get_conn(self):
        engine = self.get_engine()
        conn = engine.connect()
        return conn

    def create_session(self):
        conn = self.get_conn()
        Session = sessionmaker(bind=conn)
        session = Session()
        return session

# initialize/create datalake.db
if __name__ == '__main__':
    tdb = DatabaseUtil()
    tdb.init_db()
