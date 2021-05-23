import uvicorn
from fastapi import FastAPI
from app.routers import token, query, users

app = FastAPI()
app.include_router(token.router)
app.include_router(query.router)
app.include_router(users.router)

uvicorn.run(app)