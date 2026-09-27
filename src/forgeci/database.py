import os

#.getenv(..) = read environment variables

from sqlalchemy import create_engine, text

from sqlalchemy.orm import DeclarativeBase, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL") 

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not configured")

#used so SQLAlchemy models can define tables
class Base(DeclarativeBase):
    pass


#how ForgeCI connects to the database
engine = create_engine(DATABASE_URL)

#allows python to insert/read database rows
SessionLocal = sessionmaker(bind = engine)

def check_database_connection():
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT current_database()")
        )

        return result.scalar_one()