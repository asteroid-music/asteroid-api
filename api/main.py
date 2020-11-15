# configure logging
import api.logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# configure logging in database
from api.database import database

from api import __api_version__
import logging

logger = logging.getLogger(__name__)

app = FastAPI()

# add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# register controller routes
from api.controller import songs_router, queue_router

app.include_router(songs_router, prefix="/music", tags=["Music"])
app.include_router(queue_router, prefix="/queue", tags=["Queue"])
# attach file routes

# health check endpoint
@app.get("/healthcheck", tags=["Health"])
async def get_health():
    return {"api": __api_version__}


# queue touch
@app.on_event("startup")
async def touch_queue():
    if not await database.queue.find_one({"name": "queue"}):
        logger.info("Creating queue document...")
        from api.models.playlist import PlaylistModel

        await database.queue.insert_one(PlaylistModel(name="queue").dict())
    else:
        logger.warning("Queue document already exists.")
