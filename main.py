from fastapi import APIRouter, HTTPException, status, Depends, FastAPI
from db.client import dbClient
from db.models.email import UserEmail
from db.schemas.email_schemas import email_list_schema, email_schema
from pydantic import BaseModel

app = FastAPI()
@app.get("/")
async def root():
    return {"message:" : "We are in maintance, please put your email for advice you when the page will be reopen"}

@app.get("/send_email")
async def email():
    return email_list_schema(dbClient.dev.oplog.rs.find())

@app.post("/send_email")
async def send_email(user: UserEmail):
    if type (searchEmail(user.email)) == UserEmail:
       raise HTTPException(status_code=status.HTTP_302_FOUND, detail="Email ya registrado")
    
    emailDict= user.dict()
    id = dbClient.dev.oplog.rs.insert_one(emailDict).inserted_id
    return UserEmail(**emailDict)


def searchEmail(email: str):
    try:
        newEmail = dbClient.dev.oplog.rs.find_one({"email" : email})
        if newEmail == None:
            return newEmail
        return UserEmail(**email_schema(newEmail))
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="No se ha encontrado el email")