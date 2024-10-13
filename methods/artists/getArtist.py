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
from geniux.types import Artist
from geniux.enums import Sort, TextFormat

class GetArtist:
    @asyncFunction
    async def getArtist(self, id: int, textFormat: TextFormat = None, includeAlbums: bool = False, includeTracks: bool = False, albumSort: Sort = None, trackSort: Sort = None) -> Union[Artist, None]:
        tasks = [self._req(
            f"artists/{id}",
            {
                "text_format": textFormat.value,
            }
            if textFormat else None
        )]

        if includeAlbums:
            tasks.append(self.getArtistAlbums(id, sort=albumSort))

        if includeTracks:
            tasks.append(self.getArtistTracks(id, sort=trackSort))

        responses = await asyncio.gather(*tasks)

        artist = responses[0]
        artist = artist.get("artist")
        if not artist:
            return

        if includeAlbums:
            artist["albums"] = responses[1]

        if includeTracks:
            artist["tracks"] = responses[1 if not includeAlbums else 2]

        return self._finalizeResponse(artist, Artist)