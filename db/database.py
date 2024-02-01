from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from config import link

engine: Engine = create_engine(link)
SessionLocal = sessionmaker(engine, autocommit=False, autoflush=False)


class Base(DeclarativeBase):
    """Declarative Base Class."""
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
