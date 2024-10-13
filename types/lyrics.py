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

from geniux.utils import unixToDatetime

from .base import Base
from .stats import Stats

class Lyrics(Base):
    def __init__(self, lyrics: dict, client: "Client" = None) -> None:
        from .user import User
        super().__init__(client)

        track = lyrics.get("track")
        trackLyrics = getattr(track, "lyrics", None) if track else None

        self.plain = lyrics.get("plain")
        self.html = lyrics.get("html")
        self.markdown = lyrics.get("markdown")
        self.markdownV2 = lyrics.get("markdownV2")

        self.instrumental = lyrics.get("instrumental") or (trackLyrics.instrumental if trackLyrics else None)
        self.state = lyrics.get("state") or (trackLyrics.state if trackLyrics else None)
        self.verified = lyrics.get("verified") or (trackLyrics.verified if trackLyrics else None)
        self.explicit = lyrics.get("explicit") or (trackLyrics.explicit if trackLyrics else None)
        self.music = lyrics.get("music") or (trackLyrics.music if trackLyrics else None)

        self.language = lyrics.get("language") or (trackLyrics.language if trackLyrics else None)

        self.lyricsPlaceholderReason = lyrics.get("lyricsPlaceholderReason") or (trackLyrics.lyricsPlaceholderReason if trackLyrics else None)
        self.hasInstagramReelAnnotations = lyrics.get("hasInstagramReelAnnotations") or (trackLyrics.hasInstagramReelAnnotations if trackLyrics else None)

        verifiedBy = lyrics.get("verifiedBy")
        self.verifiedBy = [
            self._client._finalizeResponse(
                user,
                User,
            )
            for user in verifiedBy
        ] if verifiedBy else (trackLyrics.verifiedBy if trackLyrics else None)
        markedCompleteBy = lyrics.get("markedCompleteBy")
        self.markedCompleteBy = self._client._finalizeResponse(
            markedCompleteBy,
            User,
        ) if markedCompleteBy else (trackLyrics.markedCompleteBy if trackLyrics else None)
        staffApprovedBy = lyrics.get("staffApprovedBy")
        self.staffApprovedBy = self._client._finalizeResponse(
            staffApprovedBy,
            User,
        ) if staffApprovedBy else (trackLyrics.staffApprovedBy if trackLyrics else None)

        updatedAt = lyrics.get("updatedAt")
        self.updatedAt = unixToDatetime(updatedAt) if updatedAt else (trackLyrics.updatedAt if trackLyrics else None)

        owner = lyrics.get("ownerId")
        self.owner = self._client._finalizeResponse(
            {
                "id": owner,
            },
            User,
        ) if owner else (trackLyrics.owner if trackLyrics else None)

        self.stats = self._client._finalizeResponse(
            {
                "pendingEdits": lyrics.get("pendingEdits") or (trackLyrics.stats.pendingEdits if trackLyrics else None),
                "verifiedBy": len(self.verifiedBy) if self.verifiedBy else None,
            },
            Stats,
        )

        if track:
            track.lyrics = None
            self.track = track

        else:
            self.track = None

        self.raw = lyrics