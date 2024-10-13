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

import asyncio
from typing import Union

from geniux.aio import asyncFunction
from geniux.types import Album
from geniux.enums import TextFormat

class GetAlbum:
    @asyncFunction
    async def getAlbum(self, id: int, textFormat: TextFormat = None, includeTracks: bool = False) -> Union[Album, None]:
        tasks = [self._req(
            f"albums/{id}",
            {
                "text_format": textFormat.value,
            } if textFormat else None,
        )]

        if includeTracks:
            tasks.append(self.getAlbumTracks(id))

        responses = await asyncio.gather(*tasks)

        album = responses[0]
        album = album.get("album")
        if not album:
            return

        if includeTracks:
            album["tracks"] = responses[1]

        return self._finalizeResponse(album, Album)