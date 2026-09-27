from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,Session,declarative_base


DATABASE_URL = "postgresql://postgres:asmin@localhost:5432/fastapi"


engine = create_engine(
  DATABASE_URL
)

SessionLocal = sessionmaker(
  autoflush=False,
  autocommit = False,
  bind = engine
)

Base =declarative_base()

def get_db():
  db =SessionLocal()
  try:
    yield db

  finally:
    db.close()   