from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import router as ApiRouter

app = FastAPI()

origins = [
        "http://localhost:80/",
        "http://localhost:3000/",
        ]

app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        )

# Add Routers 
# app.include_router(YourRouter)

app.include_router(ApiRouter)
