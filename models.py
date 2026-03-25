from pydantic import BaseModel
from sqlalchemy import Column, Integer, String , Boolean ,ForeignKey
from database import Base
class Mesuem_Tanks(Base):
    __tablename__="museum_tanks"
    id=Column("id",Integer,primary_key=True,index=True)
    Name=Column("name",String)
    Description=Column("description",String) #description used in database in pgadmin Description used when mapping to sql
    Country=Column("country",String)
    Year=Column("year",Integer)
class TankBase(BaseModel):
    Name : str
    Description : str
    Country : str
    Year : int    