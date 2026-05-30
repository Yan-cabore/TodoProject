from sqlalchemy import create_engine  # type: ignore[import]
from sqlalchemy.orm import sessionmaker # type: ignore[import]
from sqlalchemy.ext.declarative import declarative_base # type: ignore[import] 

SQLALCHEMY_DATABASE_URL = 'sqlite:///./todos.db'

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

