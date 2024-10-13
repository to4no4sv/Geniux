#  Geniux — Genius API Client Library for Python
#  Copyright (C) 2024—present to4no4sv <https://github.com/to4no4sv/Geniux>
#
#  This file is part of Geniux.
#
#  Geniux is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Geniux is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Geniux. If not, see <http://www.gnu.org/licenses/>.

import copy
from typing import Union, List
from datetime import datetime

from geniux.aio import asyncFunction
from geniux.config import Genius
from geniux.enums import Sort, TextFormat
from geniux.utils import parsePhoto, cleanTitle, artistsToStr

from .base import Base
from .photo import Photo
from .stats import Stats
from .coverArt import CoverArt
from .track import Track

class Album(Base, Photo):
    def __init__(self, album: dict, client: "Client" = None) -> None:
        from .artist import Artist
        super().__init__(client)

        self.title = cleanTitle(album.get("name"))

        primaryArtist = album.get("artist")
        self.primaryArtist = self._client._finalizeResponse(
            primaryArtist,
            Artist,
        ) if primaryArtist else None

        self.artist = artistsToStr(self.primaryArtist)

        self.photo = parsePhoto(album.get("cover_art_url"))
        self.header = parsePhoto(album.get("header_image_url"))

        description = album.get("description")
        self.description = description.get("plain") or description.get("dom") or description.get("html") or description.get("markdown") if description else None

        releaseDateComponents = album.get("release_date_components")
        if releaseDateComponents and all(releaseDateComponents.get(component) for component in ["day", "month", "year"]):
            day = releaseDateComponents.get("day")
            month = releaseDateComponents.get("month")
            year = releaseDateComponents.get("year")
            self.releaseDate = datetime(year, month, day).date()

        else:
            self.releaseDate = None

        description = album.get("description_preview")
        self.description = description if description else None

        self.tracks = album.get("tracks")

        self.lockState = album.get("lock_state")

        coverArts = album.get("cover_arts")
        self.coverArts = [
            self._client._finalizeResponse(
                {
                    **coverArt,
                    **{"album": copy.copy(self)},
                },
                CoverArt)
            for coverArt in coverArts
        ] if coverArts else None

        self.stats = self._client._finalizeResponse(
            {
                "tracks": (len(self.tracks) if isinstance(self.tracks, list) else 1) if self.tracks else None,
                "views": album.get("song_pageviews"),
                "pyongs": album.get("pyongs_count"),
                "comments": album.get("comment_count"),
                "coverArts": len(self.coverArts) if self.coverArts else None,
            },
            Stats,
        )

        self.id = album.get("id") or int(album.get("api_path").replace("/albums/", str()))
        url = album.get("url")
        self.artistDomain, self.albumDomain = url[url.find("/albums/") + len("/albums/"):].split("/")
        self.domain = f"{self.artistDomain}/{self.albumDomain}"

        self.url = f"{Genius}albums/{self.domain}"

        self.raw = album


    @asyncFunction
    async def get(self, textFormat: TextFormat = None, includeTracks: bool = False) -> "Album":
        return await self._client.getAlbum(self.id, textFormat, includeTracks)


    @asyncFunction
    async def getTracks(self, perPage: int = 50, page: int = 1, sort: Sort = None) -> Union[List[Track], Track, None]:
        return await self._client.getAlbumTracks(self.id, perPage, page, sort)