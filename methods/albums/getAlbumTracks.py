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
from typing import Union, List

from geniux.aio import asyncFunction
from geniux.types import Track
from geniux.enums import Sort

class GetAlbumTracks:
    @asyncFunction
    async def getAlbumTracks(self, id: int, perPage: int = None, page: int = None, sort: Sort = None) -> Union[List[Track], Track, None]:
        tracks = await self._req(
            f"albums/{id}/tracks",
            {
                "per_page": perPage,
                "page": page,
                **({"sort": sort.value}
                if sort else dict()),
            },
        )

        tracks = tracks.get("tracks")
        for idx, trackInfo in enumerate(tracks):
            track = trackInfo.get("song")
            track["number"] = trackInfo.get("number")

            tracks[idx] = track

        return self._finalizeResponse(tracks, Track)