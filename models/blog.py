from db.database import Base
from sqlalchemy import Column, Integer, String,Text, ForeignKey
from sqlalchemy.orm import relationship



class DbBlog(Base):
    __tablename__ = 'blogs'

    id = Column(Integer,primary_key=True, index=True)
    title = Column(String,nullable=False)
    content = Column(Text,nullable=False)

    user_id = Column(Integer,ForeignKey('users.id'))

    user = relationship('DbUser',back_populates='blogs')
