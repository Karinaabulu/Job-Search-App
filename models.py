from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    nin = Column(String, unique=True, index=True)
    full_name = Column(String)
    date_of_birth = Column(String)
    desired_job = Column(String, nullable=True)
    passport_photo_path = Column(String, nullable=True)
    cv_path = Column(String, nullable=True)
    payment_status = Column(String, default="unpaid")