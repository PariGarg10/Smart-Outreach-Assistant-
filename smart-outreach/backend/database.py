from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

engine = create_engine("sqlite:///outreach.db")

SessionLocal = sessionmaker(bind=engine)

# Create tables
Base.metadata.create_all(engine)