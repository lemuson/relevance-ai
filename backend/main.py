from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from API.routes.evaluation_router import router

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5173",   # Vite dev server
        "http://localhost:5173",   # Vite dev server
        "http://127.0.0.1:3000",   # Дополнительные адреса
        "http://localhost:3000",
    ],
    allow_credentials = True,
    allow_methods = ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers = ["*"],
)

app.include_router(router)