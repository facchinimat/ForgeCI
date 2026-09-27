from forgeci.database import Base, engine
from forgeci.models import Build

def create_tables():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    create_tables()
    print("Database tables created.")