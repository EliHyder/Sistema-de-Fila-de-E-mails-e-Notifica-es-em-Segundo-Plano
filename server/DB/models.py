# models.py
from .db import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class User(Base):
  __tablename__ = "users"

  id = Column(Integer, primary_key=True, index=True)
  name = Column(String, nullable=False)
  email = Column(String, unique=True, index=True, nullable=False)
  created_at = Column(String, nullable=False)

  logs = relationship("Logs", back_populates="user")

  def __repr__(self):
    return f"<User(name='{self.name}', email='{self.email}', created_at='{self.created_at}')>"


class Logs(Base):
    __tablename__ = "email_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    subject = Column(String, nullable=False)
    body = Column(String, nullable=False)
    status = Column(String, nullable=False)
    attempts = Column(Integer, nullable=False, default=0)
    error_message = Column(String, nullable=True)
    created_at = Column(String, nullable=False)
    updated_at = Column(String, nullable=True)

    # Define the relationship with the User model
    user = relationship("User", back_populates="logs")

    def __repr__(self):
        return f"<Logs(user_id='{self.user_id}', subject='{self.subject}', status='{self.status}', created_at='{self.created_at}', updated_at='{self.updated_at}')>"