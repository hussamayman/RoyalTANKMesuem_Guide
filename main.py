from fastapi import FastAPI , Depends , HTTPException
from database import Base, engine
from pydantic import BaseModel
import models
from database import Session_local
from typing import Annotated
from routing import router

models.Base.metadata.create_all(bind=engine) # create tables and attribuates but no data
app = FastAPI()
app.include_router(router)
def get_db():
    db=Session_local()
    try:
        yield db
    finally:
        db.close()

    
        
