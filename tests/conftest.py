import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import test_link
from core import app
from db.database import Base
from db.database import get_db

engine = create_engine(test_link)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True, scope='session')
def prepare_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
