import os, pytest, sqlalchemy as sa
from sqlalchemy import text

DB_URL = os.getenv("DB_URL", "mysql+pymysql://root:secret@mariadb:3306/vg")

@pytest.fixture(scope="session")
def engine():
    eng = sa.create_engine(DB_URL, pool_pre_ping=True)
    with eng.connect() as c:
        c.execute(text("SELECT 1"))
    return eng

@pytest.fixture(scope="function")
def conn(engine):
    with engine.begin() as c:
        yield c
