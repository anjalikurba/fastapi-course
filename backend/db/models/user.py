from db.base_class import Base
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from  .blog import Blog
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    blogs = relationship("Blog", back_populates="author")