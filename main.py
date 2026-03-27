from fastapi import FastAPI, Depends
import model
from database import engine, get_db

app = FastAPI()

model.Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
 return {"message": "FastAPI + PostgreSQL is ready!"}