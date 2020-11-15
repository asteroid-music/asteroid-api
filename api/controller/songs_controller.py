from typing import List
import re

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import HttpUrl

from api.database import database, unravell_cursor
from api.models import Message
from api.models.songs import SongsOut, SongsModel
from api.services.requester import Requester

songs_router = APIRouter()
collection = database.get_collection("songs")


async def is_duplicate_url(url):
    return await collection.find_one({"url": url})


async def add_to_database(song: SongsModel):
    document = song.dict()
    result = await collection.insert_one(document)

    # update id
    document["_id"] = result.inserted_id
    return document


@songs_router.get("/songs", response_model=List[SongsOut])
async def get_all_songs():
    """ get all songs in database """
    return await unravell_cursor(collection.find())


@songs_router.post(
    "/songs",
    status_code=201,
    response_model=SongsOut,
    responses={400: {"message": Message}},
)
async def add_song(url: HttpUrl):
    """ add new song by url """
    # check if duplicate
    url = url.split("&")[0]  # drop additional query terms
    if await is_duplicate_url(url):
        return JSONResponse(status_code=400, content={"message": "duplicate"})

    # fetch song
    requester = Requester(url)
    status = requester.fetch()

    if status != "done":
        return JSONResponse(status_code=400, content={"message": "invalid url"})

    # add to database
    song = SongsModel(**requester.song)
    return await add_to_database(song)


def regex(term: str) -> dict:
    return {"$regex": re.compile(term, re.IGNORECASE)}


@songs_router.get("/songs/{song}", response_model=List[SongsOut])
async def get_song_by_name(song: str):
    return await unravell_cursor(collection.find({"song": regex(song)}))


@songs_router.get("/artist/{artist}", response_model=List[SongsOut])
async def get_song_by_artist(artist: str):
    return await unravell_cursor(collection.find({"artist": regex(artist)}))


@songs_router.get("/album/{album}", response_model=List[SongsOut])
async def get_song_by_album(album: str):
    return await unravell_cursor(collection.find({"album": regex(artist)}))
