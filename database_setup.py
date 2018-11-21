import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
 
Base = declarative_base()


class User(Base):
            """docstring for ClassNam"""
            __tablename__ = 'user'

            name = Column(String(250), nullable = False)
            id = Column(Integer, primary_key=True)
            email = Column(String(250), nullable=False)
            picture= Column(String(250))

 
class Category(Base):
    __tablename__ = 'category'
   
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    user_id = Column(Integer,ForeignKey('user.id'))
    user = relationship(User)


    # @property
    # def serialize(self):
    #     #Return object data in easily serializeable format
    #     return {
    #     'id'     : self.id,
    #     'name' : self.name
    #     }   


                
                        
 
class Item(Base):
    __tablename__ = 'item'

    name =Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    description = Column(String(250))
    price = Column(String(8))
    picture = Column(String(250), nullable = True)
    category_id = Column(Integer,ForeignKey('category.id'))
    date_creation = Column(Date, nullable=False)
    category = relationship(Category)
    user_id = Column(Integer,ForeignKey('user.id'))
    user = relationship(User)

    

    # @property
    # def serialize(self):
    #     #Return object data in easily serializeable format
    #     return {
    #     'name'     : self.name,
    #     'description' : self.description,
    #     'id'  : self.id,
    #      'price' : self.price,
    #      'course' : self.course
    #     }
    

engine = create_engine('sqlite:///catalogitem.db')
Base.metadata.create_all(engine)