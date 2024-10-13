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

from typing import Union

from geniux.aio import asyncFunction
from geniux.config import Genius
from geniux.enums import TextFormat
from geniux.utils import unixToDatetime, clean

from .base import Base
from .stats import Stats
from .comment import Comment

class Annotation(Base):
    def __init__(self, annotation: dict, client: "Client" = None) -> None:
        from .track import Track
        from .user import User
        super().__init__(client)

        annotations = annotation.get("annotations")
        annotations = annotations[0] if annotations else annotation

        referent = annotation.get("referent")
        lyrics = annotation.get("fragment") or (referent.get("fragment") if referent else None)
        self.lyrics = clean(lyrics) if lyrics else None

        body = annotations.get("body")
        text = body.get("plain") or body.get("dom") or body.get("html") or body.get("markdown") if body else None
        self.text = text if text else None

        self.state = annotation.get("classification")
        createdAt = annotation.get("create")
        self.createdAt = unixToDatetime(createdAt) if createdAt else None

        self.description = annotation.get("is_description")
        self.image = annotation.get("is_image")
        self.beingCreated = annotation.get("being_created")
        self.community = annotations.get("community")
        self.deleted = annotations.get("deleted")
        self.verified = annotations.get("verified")
        self.hasVoters = annotations.get("has_voters")
        self.source = annotations.get("source")

        self.customPreview = annotations.get("custom_preview")

        acceptedBy = annotations.get("accepted_by")
        self.acceptedBy = self._client._finalizeResponse(
            acceptedBy,
            User,
        ) if acceptedBy else None

        verifiedBy = annotations.get("verified_by")
        self.verifiedBy = self._client._finalizeResponse(
            verifiedBy,
            User,
        ) if verifiedBy else None

        rejectionComment = annotations.get("rejection_comment")
        self.rejectionComment = self._client._finalizeResponse(
            rejectionComment,
            Comment,
        ) if rejectionComment else None

        topComment = annotations.get("top_comment")
        self.topComment = self._client._finalizeResponse(
            topComment,
            Comment,
        ) if topComment else None

        authors = annotations.get("authors")
        if authors:
            for idx, authorInfo in enumerate(authors):
                author = authorInfo.get("user")
                author["annotationImpact"] = authorInfo.get("attribution")

                authors[idx] = author

            self.authors = [
                self._client._finalizeResponse(
                    author,
                    User,
                )
                for author in authors
            ]

        else:
            author = annotation.get("author")
            self.authors = [
                self._client._finalizeResponse(
                    author,
                    User,
                )
            ] if author else None

        verifiedByIds = annotations.get("verified_annotator_ids")
        self.verifiedBy = [
            self._client._finalizeResponse(
                {
                    "id": verifiedById,
                },
                User,
            )
            for verifiedById in verifiedByIds
        ] if verifiedByIds else None

        track = annotation.get("annotatable")
        self.track = self._client._finalizeResponse(
            track,
            Track,
        ) if track else None

        self.stats = self._client._finalizeResponse(
            {
                "votes": annotations.get("votes_total"),
                "pendingEdits": annotations.get("proposed_edit_count"),
                "comments": annotations.get("comment_count"),
                "pyongs": annotations.get("pyongs_count"),
                "authors": len(self.authors) if self.authors else None,
                "verifiedBy": len(self.verifiedBy) if self.verifiedBy else None,
            },
            Stats,
        )

        self.id = annotation.get("id") or int(annotation.get("api_path").replace("/referents/", str()))
        self.url = f"{Genius}{self.id}"

        self.raw = annotation


    @asyncFunction
    async def get(self, textFormat: TextFormat = None) -> Union["Annotation", None]:
        return await self._client.getAnnotation(self.id, textFormat)