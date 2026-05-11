from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Outreach(Base):
    __tablename__ = "outreach"

    email = Column(String, primary_key=True)
    name = Column(String)
    company = Column(String)
    role = Column(String)
    status = Column(String)  # pending / sent / replied