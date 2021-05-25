from fastapi import FastAPI
from .routers import users, token, query


app = FastAPI()
app.include_router(users.router)
app.include_router(token.router)
app.include_router(query.router)