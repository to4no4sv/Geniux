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

class Question(Base):
    def __init__(self, question: dict, client: "Client" = None) -> None:
        from .album import Album
        from .annotation import Annotation
        from .track import Track
        from .user import User
        from .answer import Answer
        super().__init__(client)

        text = question.get("body")
        self.text = text if text else None

        createdAt = question.get("created_at")
        self.createdAt = unixToDatetime(createdAt) if createdAt else None

        self.state = question.get("state")
        self.pinOrder = question.get("pin_order")
        self.hasVoters = question.get("has_voters")
        self.defaultKey = question.get("default_key")
        self.defaultQuestion = question.get("default_question")

        author = question.get("author")
        self.author = self._client._finalizeResponse(
            author,
            User,
        ) if author else None

        questionableType = question.get("questionable_type")
        self.questionableType = Track if questionableType == "song" else (Annotation if questionableType == "annotation" else (Album if questionableType == "album" else ...))

        questionable = question.get("questionable")
        self.questionable = self._client._finalizeResponse(
            questionable,
            self.questionableType,
        ) if self.questionableType and questionable else None

        answer = question.get("answer")
        self.answer = self._client._finalizeResponse(
            answer,
            Answer,
        ) if answer else None

        self.stats = self._client._finalizeResponse(
            {
                "votes": question.get("votes_total"),
                "contributors": question.get("contributors_count"),
            },
            Stats,
        )

        self.id = question.get("id")
        self.url = question.get("url")

        self.raw = question