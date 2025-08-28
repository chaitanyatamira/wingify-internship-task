from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Analysis(Base):
    __tablename__ = "analyses"
    id = Column(Integer, primary_key=True, autoincrement=True)
    file_name = Column(String(255), nullable=False)
    query = Column(Text, nullable=False)
    analysis = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)