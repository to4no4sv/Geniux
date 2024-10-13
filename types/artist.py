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

from typing import Union, List

from geniux.aio import asyncFunction
from geniux.config import Genius
from geniux.utils import parsePhoto, cleanArtists
from geniux.enums import Sort, TextFormat
from .base import Base
from .photo import Photo
from .stats import Stats
from .album import Album
from .track import Track

class Artist(Base, Photo):
    def __init__(self, artist: dict, client: "Client" = None) -> None:
        from .user import User
        super().__init__(client)

        self.nickname = cleanArtists(artist.get("name"))
        alternativeNicknames = artist.get("alternate_names")
        self.alternativeNicknames = [cleanArtists(alternativeNickname) for alternativeNickname in alternativeNicknames] if alternativeNicknames else None

        self.photo = parsePhoto(artist.get("image_url"))
        self.header = parsePhoto(artist.get("header_image_url"))

        description = artist.get("description")
        self.description = description.get("plain") or description.get("dom") or description.get("html") or description.get("markdown") if description else None

        self.indexCharacter = artist.get("index_character")
        self.memeVerified = artist.get("is_meme_verified")
        self.verified = artist.get("is_verified")
        self.translation = artist.get("translation_artist")

        self.instagram = artist.get("instagram_name")
        self.twitter = artist.get("twitter_name")
        self.facebook = artist.get("facebook_name")

        self.albums = artist.get("albums")
        self.tracks = artist.get("tracks")

        user = artist.get("user")
        self.user = self._client._finalizeResponse(
            user,
            User,
        ) if user else None

        self.role = artist.get("role")
        self.stats = self._client._finalizeResponse(
            {
                "followers": artist.get("followers_count"),
                "IQ": artist.get("iq"),
            },
            Stats,
        )

        self.id = artist.get("id")
        self.domain = artist.get("slug")
        self.url = f"{Genius}artists/{self.domain}"

        self.raw = artist


    @asyncFunction
    async def get(self, textFormat: TextFormat = None, includeAlbums: bool = False, includeTracks: bool = False, albumSort: Sort = None, trackSort: Sort = None) -> "Artist":
        return await self._client.getArtist(self.id, textFormat, includeAlbums, includeTracks, albumSort, trackSort)


    @asyncFunction
    async def getAlbums(self, perPage: int = None, page: int = None, sort: Sort = None) -> Union[List[Album], Album, None]:
        return await self._client.getArtistAlbums(self.id, perPage, page, sort)


    @asyncFunction
    async def getTracks(self, perPage: int = None, page: int = None, sort: Sort = None) -> Union[List[Track], Track, None]:
        return await self._client.getArtistTracks(self.id, perPage, page, sort)