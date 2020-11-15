from typing import List

from pydantic import BaseModel, Field

from api.models.songs import SongsModel, SongsOut
from api.models.objectid import ObjectId


class PlaylistItem(BaseModel):
    song: SongsModel
    votes: int


class PlaylistModel(BaseModel):
    schema_version: int = 1
    id: ObjectId = Field(None, alias="_id")

    name: str
    songs: List[PlaylistItem] = []  # bucket

    class Config:
        allow_population_by_field_name = True


class PlaylistItemOut(BaseModel):
    song: SongsOut
    votes: int


class PlaylistOut(BaseModel):
    name: str
    songs: List[PlaylistItemOut]  # bucket
