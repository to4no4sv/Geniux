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
from geniux.utils import unixToDatetime

from .base import Base
from .stats import Stats

class Comment(Base):
    def __init__(self, comment: dict, client: "Client" = None) -> None:
        from .album import Album
        from .annotation import Annotation
        from .track import Track
        from .user import User
        super().__init__(client)

        body = comment.get("body")
        text = body.get("plain") or body.get("dom") or body.get("html") or body.get("markdown") if body else None
        self.text = text if text else None

        self.state = comment.get("state")
        self.disposition = comment.get("disposition")

        createdAt = comment.get("created_at")
        self.createdAt = unixToDatetime(createdAt) if createdAt else None
        deletedAt = comment.get("deleted_at")
        self.deletedAt = unixToDatetime(deletedAt) if deletedAt else None

        self.hasVoters = comment.get("has_voters")

        self.anonymousAuthor = comment.get("anonymous_author")
        author = comment.get("author")
        self.author = self._client._finalizeResponse(
            author,
            User,
        ) if author else None

        commentableType = comment.get("commentable_type")
        self.commentableType = Track if commentableType == "Song" else (Annotation if commentableType == "Annotation" else (Album if commentableType == "Album" else ...))

        commentable = comment.get("commentable")
        self.commentable = self._client._finalizeResponse(
            commentable,
            self.commentableType,
        ) if self.commentableType and commentable else None

        self.stats = self._client._finalizeResponse(
            {
                "votes": comment.get("votes_total"),
            },
            Stats,
        )

        self.id = comment.get("id")
        self.url = f"{Genius}comments/{self.id}"

        self.raw = comment