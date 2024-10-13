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

from .base import Base

class Stats(Base):
    def __init__(self, stats: dict, client: "Client" = None) -> None:
        super().__init__(client)

        self.tracks = stats.get("tracks")
        self.votes = stats.get("votes")

        self.IQ = stats.get("IQ")

        self.followedUsers = stats.get("followedUsers")
        self.followers = stats.get("followers")

        self.roles = stats.get("roles")

        self.views = stats.get("views")
        self.concurrents = stats.get("concurrents")
        self.coverArts = stats.get("coverArts")

        self.pendingEdits = stats.get("pendingEdits")
        self.verifiedBy = stats.get("verifiedBy")

        self.contributors = stats.get("contributors")
        self.IQEarners = stats.get("IQEarners")
        self.transcribers = stats.get("transcribers")

        self.annotations = stats.get("annotations")
        self.transcribes = stats.get("transcribes")
        self.questions = stats.get("questions")
        self.answers = stats.get("answers")
        self.forumPosts = stats.get("forumPosts")

        self.verifiedAnnotations = stats.get("verifiedAnnotations")
        self.acceptedAnnotations = stats.get("acceptedAnnotations")
        self.unreviewedAnnotations = stats.get("unreviewedAnnotations")

        self.comments = stats.get("comments")
        self.pyongs = stats.get("pyongs")

        self.raw = stats