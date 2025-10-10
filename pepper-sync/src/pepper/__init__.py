from .config import Config
from .logger import logger
from .app_cache import CachedDictList
from .app_queue import QueueManager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from .types.options import ServerOption
from .routes import (devices, events, geofences, identity, positions,
                     resolvers, server, users)
# from fastapi.staticfiles import StaticFiles

config = Config()

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up the pepper-sync...")
    app.state.options = ServerOption()

    yield  # This is where the application runs

    # Shutdown logic
    logger.info("Shutting down the application...")
    # app.state.options = None

app = FastAPI(
    lifespan=lifespan,
    openapi_url="/api/openapi.json",
    docs_url="/docs/swagger",
    redoc_url="/docs",
    title=config.options.title or "None",
    description="Multiplatform sync CLI application for location tracking systems",
    version=f"{config.options.version}" or "0.1",
    terms_of_service="http://github.com/drolx/pepper-local",
    contact={
        "name": "drolx Lab",
        "url": "http://github.com/drolx/pepper-local",
        "email": "dev@drolx.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://mit-license.org/",
    },
)

# app.mount("/static", StaticFiles(directory="public"), name="static")
# app.mount("/", StaticFiles(directory="ui/dist", html=True), name="app")
app.include_router(server.router)
app.include_router(resolvers.router)
app.include_router(identity.router)
app.include_router(devices.router)
app.include_router(geofences.router)
app.include_router(positions.router)
app.include_router(events.router)
app.include_router(users.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

__all__ = ["logger", "Config", "config", "CachedDictList", "QueueManager"]
