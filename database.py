from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine=create_engine(DATABASE_URL)
Session_local=sessionmaker(autocommit=False,autoflush=False,bind=engine)#Session is used to talk to the database (queries, insert, update, delete).
Base=declarative_base() #define database tables (models).