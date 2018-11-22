import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.sql import func
#import DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
import datetime
import json
#----------------------------------
# We must install DateTime Package
#---------------------------------
 
Base = declarative_base()


class User(Base):
            """docstring for ClassNam"""
            __tablename__ = 'user'

            id = Column(Integer, primary_key=True)
            name = Column(String(250), nullable = False)
            email = Column(String(250), nullable=False)
            picture= Column(String(250))

 
class Category(Base):
    __tablename__ = 'category'
   
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    user_id = Column(Integer,ForeignKey('user.id'))
    user = relationship(User)
    items = relationship("Item")


    @property
    def serialize(self):
        #Return object data in easily serializeable format
        return {
        'id'     : self.id,
        'name' : self.name,
        'items': [item.serialize for item in self.items]
        }  
    @property
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)



                
                        
 
class Item(Base):
    __tablename__ = 'item'

    name =Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    description = Column(String(250))
    price = Column(String(8))
    picture = Column(String(250), nullable = True)
    category_id = Column(Integer,ForeignKey('category.id'))
    #date_creation = Column(DateTime(timezone=True), server_default=func.now())
    #date_creation = Column(datetime.datetime, default=datetime.datetime.today())
    #date_creation = Column(datetime.datetime, default=func.now())
    #date_creation = Column(DateTime(), default=datetime.datetime.utcnow())
    
    date_creation = Column(DateTime(timezone=True), server_default=func.now())
    date_update = Column(DateTime(timezone=True), server_default=func.now())
    category = relationship(Category, back_populates='items')
    user_id = Column(Integer,ForeignKey('user.id'))
    user = relationship(User)
#Column(db.DateTime, default=datetime.datetime.now)
    

    @property
    def serialize(self):
        #Return object data in easily serializeable format
        return {
        'name'     : self.name,
        'description' : self.description,
        'id'  : self.id,
         'price' : self.price,
         #'date_update' : self.date_update,
         'picture'     : self.picture    
        }
    @property
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

engine = create_engine('sqlite:///catalogitems.db')
Base.metadata.create_all(engine)