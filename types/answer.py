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

class Answer(Base):
    def __init__(self, answer: dict, client: "Client" = None) -> None:
        from .user import User
        from .question import Question
        super().__init__(client)

        body = answer.get("body")
        text = body.get("plain") or body.get("dom") or body.get("html") or body.get("markdown") if body else None
        self.text = text if text else None

        textForEdit = answer.get("body_for_edit")
        self.textForEdit = textForEdit if textForEdit else None

        createdAt = answer.get("created_at")
        self.createdAt = unixToDatetime(createdAt) if createdAt else None

        self.state = answer.get("editorial_state")
        self.source = answer.get("answer_source")
        self.hasVoters = answer.get("has_voters")

        authors = answer.get("authors")
        if authors:
            for idx, authorInfo in enumerate(authors):
                author = authorInfo.get("user")
                author["answerImpact"] = authorInfo.get("attribution")

                authors[idx] = author

            self.authors = [
                self._client._finalizeResponse(
                    author,
                    User,
                )
                for author in authors
            ]

        else:
            author = answer.get("author")
            self.authors = [
                self._client._finalizeResponse(
                    author,
                    User,
                )
            ] if author else None

        question = answer.get("question")
        self.question = self._client._finalizeResponse(
            question,
            Question,
        ) if question else None

        self.stats = self._client._finalizeResponse(
            {
                "votes": answer.get("votes_total"),
                "authors": len(self.authors) if self.authors else None,
            },
            Stats,
        )

        self.id = answer.get("id")

        self.raw = answer