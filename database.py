from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 📌 SQLite
DATABASE_URL = "sqlite:///./bot.db"

# Agar PostgreSQL ishlatsangiz:
# DATABASE_URL = "postgresql+psycopg2://user:password@localhost:5432/dbname"

# Engine yaratamiz
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)

# Session yaratuvchi
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# 📌 Model yaratish uchun Base
Base = declarative_base()


# 📌 DB sessiya olish funksiyasi
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
