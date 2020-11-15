from pydantic import BaseModel, Field, FilePath, HttpUrl

from api.models.objectid import ObjectId


class SongsModel(BaseModel):
    schema_version: int = 1
    id: ObjectId = Field(None, alias="_id")
    artist: str
    album: str
    song: str
    duration: int
    file: FilePath
    url: HttpUrl

    def dict(self, *args, **kwargs):  # override method
        ret = super().dict(*args, **kwargs)
        for i in ["file", "url"]:
            ret[i] = str(ret[i])
        return ret

    class Config:
        underscore_attrs_are_private = False
        allow_population_by_field_name = True


class SongsOut(BaseModel):
    id: ObjectId = Field(..., alias="_id")

    artist: str
    album: str
    song: str

    duration: int

    class Config:
        underscore_attrs_are_private = False
        allow_population_by_field_name = True
