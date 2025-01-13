from fastapi import FastAPI
from handlers import crud_router

app: FastAPI = FastAPI()

app.include_router(crud_router)
