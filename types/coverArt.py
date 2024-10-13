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

from geniux.config import Genius
from geniux.utils import parsePhoto

from .base import Base
from .photo import Photo

class CoverArt(Base, Photo):
    def __init__(self, coverArt: dict, client: "Client" = None) -> None:
        super().__init__(client)

        self.photo = parsePhoto(coverArt.get("image_url"))

        self.annotated = coverArt.get("annotated")

        album = coverArt.get("album")
        if album:
            album.coverArts = None
        self.album = album

        self.id = coverArt.get("id")
        self.url = f"{Genius}album_cover_arts/{self.id}"

        self.raw = coverArt