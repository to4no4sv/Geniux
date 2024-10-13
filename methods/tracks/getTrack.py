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
from geniux.types import Track
from geniux.enums import TextFormat

class GetTrack:
    @asyncFunction
    async def getTrack(self, id: int, textFormat: TextFormat = None, includeLyrics: bool = False) -> Union[Track, None]:
        tasks = [self._req(
            f"songs/{id}",
            {
                "text_format": textFormat.value,
            }
            if textFormat else None,
        )]

        if includeLyrics:
            tasks.append(self.getLyrics(id))

        responses = await asyncio.gather(*tasks)

        track = responses[0]
        track = track.get("song")
        if not track:
            return

        if includeLyrics:
            track["lyrics"] = responses[1]

        return self._finalizeResponse(track, Track)