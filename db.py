from enum import unique
from numpy import integer
from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float ,DateTime
from datetime import date, datetime
from sqlalchemy.orm import sessionmaker 

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer,primary_key=True)
    username = Column(String,unique=True)
    password = Column(String)

    def __str__(self):
        return self.username

class ParkingSpace(Base):
    __tablename__ = 'Parking_space'
    id = Column(Integer,primary_key=True)
    parking_area = Column(String,unique = True) 
    free_space= Column(Integer , default = 0)
    total_space = Column(Integer,default = 0) 
    reserved_space=Column(Integer,default=0)
    date= Column(DateTime,default = datetime.now)
    time  = Column(DateTime,default = datetime.now)

    def __str__(self):
        return self.title

 
engine = create_engine("sqlite:///Carpark.sqlite",echo = True)
Base.metadata.create_all(engine)