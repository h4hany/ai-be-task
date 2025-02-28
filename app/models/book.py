from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from sqlalchemy.orm import relationship
from ..database import Base

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    gutenberg_id = Column(Integer)
    title = Column(String)
    author = Column(String)
    content = Column(String)
    book_metadata = Column(JSON)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    user = relationship("User") 