from fastapi import FastAPI , Depends , HTTPException , APIRouter ,UploadFile
from database import Base, engine
from pydantic import BaseModel
import models
from database import Session_local
from typing import Annotated
from sqlalchemy.orm import Session
from models import Mesuem_Tanks , TankBase
from Predict import load_model,preprocess , get_class_names
import torch
from Chat import chat_with_gpt

router=APIRouter()
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model, _ = load_model(device)
class_names = get_class_names()
def get_db():
    db=Session_local()
    try:
        yield db
    finally:
        db.close()
@router.post("/tanks/")
def create_tank( tank: TankBase, db: Session = Depends(get_db)):
    tank_info=models.Mesuem_Tanks(Name=tank.Name,Description=tank.Description,Country=tank.Country,Year=tank.Year)
    db.add(tank_info)
    db.commit()
    db.refresh(tank_info)
    return tank_info
@router.post("/tanks/info/{Question}")
async def tank_info(file: UploadFile,  db: Session = Depends(get_db), Question: str = ""): #to send image you need post request
    
    image_bytes = await file.read()        # 1. read file
    tensor = preprocess(image_bytes)       # 2. preprocess

    with torch.no_grad():
        outputs = model(tensor.to(device)) # 3. predict
        probs = torch.softmax(outputs, dim=1)[0]
        _, idx = torch.max(probs, 0)
    tank_name = class_names[idx.item()]    
    
    
    Tank_info = db.query(Mesuem_Tanks).filter(Mesuem_Tanks.Name == tank_name).first()
    response = chat_with_gpt(Question, Tank_info)
    if not Tank_info:
        raise HTTPException(status_code=404, detail="no match")

    return {
        "prediction_index": idx.item(),
        "tank_info": Tank_info,
        "chatbot_response": response
    }
@router.get("/tanks/list/")
def list_tanks(db : Session=Depends(get_db)):
    tanks=db.query(Mesuem_Tanks).all()
    if not tanks:
        raise HTTPException(status_code=404,detail="no match")
    return tanks

