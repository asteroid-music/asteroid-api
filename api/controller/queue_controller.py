from typing import List
from bson.objectid import ObjectId

from fastapi import APIRouter
from fastapi.responses import JSONResponse

import pymongo.errors

from api.database import database, unravell_cursor
from api.models import Message
from api.models.playlist import PlaylistModel, PlaylistOut

import logging

logger = logging.getLogger(__name__)

queue_router = APIRouter()
collection = database.get_collection("queue")
songs_collection = database.get_collection("songs")


async def fetch_song(song_id: ObjectId):
    return await songs_collection.find_one(song_id)


async def update_vote(song_id: ObjectId):
    # EAFP
    return_value = 0
    try:
        return_value = await collection.update_one(
            {"name": "queue", "songs.song._id": song_id},
            {"$inc": {"songs.$.votes": 1}},
        )

    except pymongo.errors.WriteError as e:
        logger.warning(e)
    except Exception as e:
        logger.error(e)
    else:
        return_value = return_value.modified_count

    return return_value


@queue_router.get("/", response_model=PlaylistOut)
async def get_queue():
    ret = await collection.find_one({"name": "queue"})
    print(ret)
    return ret


@queue_router.post("/", status_code=201, responses={400: {"message": "bad songid"}})
async def vote_for_song(song_id: str):
    song_id = ObjectId(song_id)

    # check song is valid
    song = await fetch_song(song_id)
    if not song:
        # song invalid
        return JSONResponse(status_code=400, content={"message": "bad songid"})

    # check if in queue, and if it is, update the vote
    if await update_vote(song_id):
        # done
        logger.info("Vote updated")
    else:
        # add song to queue
        await collection.update_one(
            {"name": "queue"}, {"$push": {"songs": {"song": song, "votes": 1}}}
        )
        logger.info("New song added to queue")

    return {"message": "ok"}
