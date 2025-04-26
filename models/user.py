from db.database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship



class DbUser(Base):
    __tablename__ = 'users'

    id = Column(Integer,primary_key=True, index=True)
    username = Column(String,nullable=False)
    email = Column(String,unique=True,nullable=False)
    password = Column(String,nullable=False)

    blogs = relationship('DbBlog',back_populates='user')


