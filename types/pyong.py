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

class Pyong(Base):
    def __init__(self, pyong: dict, client: "Client" = None) -> None:
        from .album import Album
        from .annotation import Annotation
        from .track import Track
        from .user import User
        super().__init__(client)

        body = pyong.get("note")
        text = body.get("plain") or body.get("dom") or body.get("html") or body.get("markdown") if body else None
        self.text = text if text else None

        createdAt = pyong.get("created_at")
        self.createdAt = unixToDatetime(createdAt) if createdAt else None

        user = pyong.get("user")
        self.user = self._client._finalizeResponse(
            user,
            User,
        ) if user else None

        pyongableType = pyong.get("pyongable_type")
        self.pyongableType = Track if pyongableType == "song" else (Annotation if pyongableType == "annotation" else (Album if pyongableType == "album" else ...))

        pyongable = pyong.get("pyongable")
        self.pyongable = self._client._finalizeResponse(
            pyongable,
            self.pyongableType,
        ) if self.pyongableType and pyongable else None

        self.id = pyong.get("id")

        self.raw = pyong