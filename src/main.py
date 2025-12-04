from fastapi import FastAPI
from src.auth.models import Base
from .auth.router import router as auth_router


app = FastAPI(tiltle="Taskflow API")

# include the router
app.include_router(auth_router)

@app.get("/")
def root():
    return {"message": "The server is working!"}