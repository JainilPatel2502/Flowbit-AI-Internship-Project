from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
app = FastAPI()
class Tone(BaseModel):
    email:str
    tone:str
class Total(BaseModel):
    email:str
    total:int
@app.get('/risk_alert')
def risk_alert(req:Tone):
    print(f"Coustomer {req.email} is {req.tone}")
    return {}
@app.get('/total')
def total(req:Total):
    print(f"There is qutation of {req.total} by coutomer {req.email}")
    return {}
    