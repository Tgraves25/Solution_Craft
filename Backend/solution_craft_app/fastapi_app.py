from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi import APIRouter
from pydantic import BaseModel
from fastapi.responses import JSONResponse

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Token schema
class Token(BaseModel):
    access_token: str
    token_type: str

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    return {"access_token": "fake_token", "token_type": "bearer"}

@app.get("/")
def read_root():
    return {"message": "FastAPI is running"}

api_router = APIRouter()

@api_router.get("/items/")
def read_items():
    return {"message": "FastAPI items"}

app.include_router(api_router)
