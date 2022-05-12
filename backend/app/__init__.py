from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise

from .api import router as ApiRouter
from .settings import get_settings

settings = get_settings()

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

register_tortoise(
    app,
    db_url=settings.DB_URL,
    modules={
        "models": [
            "activities.models",
            "facts.models",
            "riddles.models",
            "websites.models",
        ]
    },
    generate_schemas=True,
    add_exception_handlers=True,
)
