from fastapi import FastAPI
from app_users.routers import users_v2, users_v1

app  = FastAPI()

app.include_router(users_v1.router)
app.include_router(users_v2.router)