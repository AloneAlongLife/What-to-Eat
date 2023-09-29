from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import Server, Config

from config import HOST, PORT

from .routers import (
    article_router,
    oauth_router,
    restaurant_router,
    user_router,
)

app = FastAPI(
    root_path="",
    version="1.0.0",
)
app.include_router(article_router)
app.include_router(oauth_router)
app.include_router(restaurant_router)
app.include_router(user_router)

origins = [
    "*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def run():
    config = Config(
        app=app,
        host=HOST,
        port=PORT,
    )
    server = Server(config=config)
    await server.serve()
