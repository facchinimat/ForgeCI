import os

#.getenv(..) = read enviroment variables

from sqlalchemy import create_engine, text

DATABASE_URL = os.getenv("DATABASE_URL") #Read the value stored in the operating system under DATABASE_URL. url login is saved in terminal to avoid commiting private keys/passwords to github. 

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not configured")

#how ForgeCI connects to the database
engine = create_engine(DATABASE_URL)

def check_database_connection():
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT current_database()")
        )

        return result.scalar_one()