from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from config import psql_url

engine = create_engine(url=psql_url)

session = scoped_session(sessionmaker(bind=engine))
