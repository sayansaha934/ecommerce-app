from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from config import config
Base = declarative_base()

engine = create_engine(config.DATABASE_URL)
SESSION: Session = sessionmaker(bind=engine)()