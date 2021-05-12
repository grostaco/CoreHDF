from fastapi import FastAPI
from .routers import users, token


app = FastAPI()
app.include_router(users.router)
app.include_router(token.router)
