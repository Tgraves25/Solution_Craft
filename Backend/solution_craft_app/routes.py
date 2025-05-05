# routes.py
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

@router.post("/api/token/")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username == "test" and form_data.password == "test":
        return {"access_token": "fake_token", "token_type": "bearer"}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")
