# SQLAlchemy se database connection banane ke liye imports
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


# SQLite database ka path
# Isse project folder me taskflow.db file banegi
DATABASE_URL = "sqlite:///./taskflow.db"


# Database engine create karta hai
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)


# Database session banane ke liye
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# Saare database models isi Base se inherit karenge
Base = declarative_base()


# Har API request ke liye database session provide karega
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()