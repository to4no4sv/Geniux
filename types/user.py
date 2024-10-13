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

from typing import Union, List

from geniux.aio import asyncFunction
from geniux.config import Genius
from geniux.enums import Sort, TextFormat, Role
from geniux.utils import parsePhoto, cleanArtists

from .base import Base
from .stats import Stats
from .photo import Photo
from .annotation import Annotation
from .track import Track
from .comment import Comment
from .pyong import Pyong
from .question import Question
from .answer import Answer

class User(Base, Photo):
    def __init__(self, user: dict, client: "Client" = None) -> None:
        from .artist import Artist
        super().__init__(client)

        self.nickname = cleanArtists(user.get("name"))
        self.login = user.get("login")

        alternativeNicknames = user.get("alternate_names")
        self.alternativeNicknames = [cleanArtists(alternativeNickname) for alternativeNickname in alternativeNicknames] if alternativeNicknames else None

        avatar = user.get("avatar")
        if avatar:
            avatar = avatar.get("medium") or avatar.get("small") or avatar.get("thumb") or avatar.get("tiny")

        self.photo = parsePhoto(user.get("photo_url")) or (avatar.get("url") if avatar else None)
        self.header = parsePhoto(user.get("header_image_url"))

        description = user.get("about_me_summary")
        self.description = description if description else None

        roles = user.get("roles_for_display")
        artist = user.get("artist")

        self.memeVerified = artist and "verified_artist" not in roles if roles and artist else user.get("is_meme_verified")
        self.verified = artist and "verified_artist" in roles if roles and artist else user.get("is_verified")

        self.roles = [Role(role.replace("_a", "A")) for role in roles] if roles else None
        self.annotationImpact = user.get("annotationImpact")
        self.answerImpact = user.get("answerImpact")

        self.artist = Artist(artist, client=self._client) if artist else None

        stats = user.get("stats")
        if stats:
            annotationCount = stats.get("annotations_count")
            transcribeCount = stats.get("transcriptions_count")
            commentCount = stats.get("comments_count")
            questionCount = stats.get("questions_count")
            answerCount = stats.get("answers_count")
            forumPostCount = stats.get("forum_posts_count")
            pyongCount = stats.get("pyongs_count")

        else:
            annotationCount = None
            transcribeCount = None
            commentCount = None
            questionCount = None
            answerCount = None
            forumPostCount = None
            pyongCount = None

        self.stats = self._client._finalizeResponse(
            {
                "iq": user.get("iq"),
                "followedUsers": user.get("followed_users_count"),
                "followers": user.get("followers_count"),
                "roles": len(self.roles) if self.roles else None,
                "annotations": annotationCount,
                "transcribes": transcribeCount,
                "questions": questionCount,
                "answers": answerCount,
                "forumPosts": forumPostCount,
                "comments": commentCount,
                "pyongs": pyongCount,
            },
            Stats,
        )

        self.id = user.get("id")
        self.url = f"{Genius}{self.login}" if self.login else None

        self.raw = user


    @asyncFunction
    async def get(self) -> "User":
        return await self._client.getUser(self.id)


    @asyncFunction
    async def getActivities(self, perPage: int = None, page: int = None, sort: Sort = None, textFormat: TextFormat = None) -> Union[List[Union[Annotation, Track, Question, Answer, Comment, Pyong]], Annotation, Track, Question, Answer, Comment, Pyong, None]:
        return await self._client.getUserActivities(self.id, perPage, page, sort, textFormat)


    @asyncFunction
    async def getAnnotations(self, perPage: int = None, page: int = None, sort: Sort = None, textFormat: TextFormat = None) -> Union[List[Annotation], Annotation, None]:
        return await self._client.getUserAnnotations(self.id, perPage, page, sort, textFormat)


    @asyncFunction
    async def getTranscribes(self, perPage: int = None, page: int = None, sort: Sort = None) -> Union[List[Track], Track, None]:
        return await self._client.getUserTranscribes(self.id, perPage, page, sort)


    @asyncFunction
    async def getQuestionsAndAnswers(self, perPage: int = None, page: int = None, textFormat: TextFormat = None) -> Union[List[Union[Question, Answer]], Question, Answer, None]:
        return await self._client.getUserQuestionsAndAnswers(self.id, perPage, page, textFormat)


    @asyncFunction
    async def getComments(self, perPage: int = None, page: int = None, textFormat: TextFormat = None) -> Union[List[Comment], Comment, None]:
        return await self._client.getUserComments(self.id, perPage, page, textFormat)


    @asyncFunction
    async def getPyongs(self, perPage: int = None, page: int = None, textFormat: TextFormat = None) -> Union[List[Pyong], Pyong, None]:
        return await self._client.getUserPyongs(self.id, perPage, page, textFormat)