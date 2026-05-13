from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine

DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/postgres"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(blind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try :
        yield db
    finally:
        db.close()
