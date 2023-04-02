from fastapi import APIRouter, HTTPException, status, Depends, FastAPI
from db.client import dbClient
from db.models.email import UserEmail
from db.schemas.email_schemas import email_list_schema, email_schema
from pydantic import BaseModel
import re

app = FastAPI()
@app.get("/")
async def root():
    return {"message:" : "We are in maintance, please put your email for advice you when the page will be reopen"}

@app.get("/send_email")
async def email():
    return email_list_schema(dbClient.dev.oplog.rs.find())

@app.post("/send_email")
async def send_email(user: UserEmail):
    if es_correo_valido(user.email):
        if type (searchEmail(user.email)) == UserEmail:
            raise HTTPException(status_code=status.HTTP_302_FOUND, detail="Email ya registrado")
    
        emailDict= user.dict()
        id = dbClient.dev.oplog.rs.insert_one(emailDict).inserted_id
        return UserEmail(**emailDict)
    else: 
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No es un correo electrónico")


def searchEmail(email: str):
    try:
        newEmail = dbClient.dev.oplog.rs.find_one({"email" : email})
        if newEmail == None:
            return newEmail
        return UserEmail(**email_schema(newEmail))
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="No se ha encontrado el email")
    
def es_correo_valido(correo):
    expresion_regular = r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"
    return re.match(expresion_regular, correo)