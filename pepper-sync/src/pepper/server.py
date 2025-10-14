import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_crons import Crons  # pyright: ignore[reportMissingTypeStubs]
from fastapi_crons import get_cron_router  # pyright: ignore[reportMissingTypeStubs]
from fastapi_crons.state import SQLiteStateBackend  # pyright: ignore[reportMissingTypeStubs]

from pepper import config, logger
from pepper.db import register_orm
from pepper.process_queue import device_cache_queue, position_storage_queue
from pepper.routes import forward
from tortoise import Tortoise

from .resolvers import load_resolver_jobs
from .routes import (devices, events, geofences, identity, positions,
                     resolvers, server, users)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up the pepper-sync...")
    asyncio.create_task(device_cache_queue())
    asyncio.create_task(position_storage_queue())

    async with register_orm(app):
        yield
        

    # This is where the application runs
    yield

    # NOTE: Shutdown logic
    logger.info("Shutting down the application...")
    await Tortoise.close_connections()


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
state = SQLiteStateBackend(db_path="db-tasks.sqlite3")
crons = Crons(app, state_backend=state)
resolver_jobs = load_resolver_jobs()
for job in resolver_jobs:
    crons.jobs.append(job)


app.mount("/static", StaticFiles(directory="public"), name="static")
# app.mount("/", StaticFiles(directory="ui/dist", html=True), name="app")
app.include_router(server.router)
app.include_router(forward.router)
app.include_router(get_cron_router(), prefix="/api/tasks", tags=["tasks"])
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
