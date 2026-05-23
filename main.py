from fastapi import FastAPI , Depends , HTTPException
from database import Base, engine
from pydantic import BaseModel
import models
from database import Session_local
from typing import Annotated
from routing import router
from contextlib import asynccontextmanager
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("App starting...")
    models.Base.metadata.create_all(bind=engine)
    yield
    print("App shutting down...")
    
app = FastAPI()
app.include_router(router)

    
        
