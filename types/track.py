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

import copy
from typing import Union, List
from datetime import datetime

from geniux.aio import asyncFunction
from geniux.config import Genius
from geniux.enums import TextFormat, Role, Color
from geniux.utils import unixToDatetime, parsePhoto, cleanTitle, artistsToStr

from .base import Base
from .stats import Stats
from .photo import Photo
from .lyrics import Lyrics
from .genre import Genre
from .annotation import Annotation

class Track(Base, Photo):
    def __init__(self, track: dict, client: "Client" = None) -> None:
        from .artist import Artist
        from .album import Album
        from .user import User
        super().__init__(client)

        self.title = cleanTitle(track.get("title"))

        primaryArtist = track.get("primary_artist")
        self.primaryArtist = self._client._finalizeResponse(
            primaryArtist,
            Artist,
        ) if primaryArtist else None

        featuredArtists = track.get("featured_artists")
        self.featuredArtists = [
            self._client._finalizeResponse(
                featuredArtist,
                Artist,
            )
            for featuredArtist in featuredArtists
        ] if featuredArtists else None

        self.artist = artistsToStr(self.primaryArtist, self.featuredArtists)

        producers = track.get("producer_artists")
        self.producers = [
            self._client._finalizeResponse(
                producer,
                Artist,
            )
            for producer in producers
        ] if producers else None

        writers = track.get("writer_artists")
        self.writers = [
            self._client._finalizeResponse(
                writer,
                Artist,
            )
            for writer in writers
        ] if writers else None

        self.photo = parsePhoto(track.get("song_art_image_url"))
        self.header = parsePhoto(track.get("header_image_url"))

        description = track.get("description")
        self.description = description.get("plain") or description.get("dom") or description.get("html") or description.get("markdown") if description else None

        self.primaryColor = track.get("song_art_primary_color")
        self.secondColor = track.get("song_art_secondary_color")
        textColor = track.get("song_art_text_color")
        self.textColor = (Color.White if textColor == "#fff" else Color.Black) if textColor else None

        releaseDateComponents = track.get("release_date_components")
        if releaseDateComponents and all(releaseDateComponents.get(component) for component in ["day", "month", "year"]):
            day = releaseDateComponents.get("day")
            month = releaseDateComponents.get("month")
            year = releaseDateComponents.get("year")
            self.releaseDate = datetime(year, month, day).date()

        else:
            self.releaseDate = None

        primaryGenre = track.get("primary_tag")
        self.primaryGenre = self._client._finalizeResponse(
            primaryGenre,
            Genre,
        ) if primaryGenre else None

        genres = track.get("tags")
        self.genres = [
            self._client._finalizeResponse(
                genre,
                Genre,
            )
            for genre in genres
        ] if genres else None

        albums = track.get("albums")
        self.albums = [
            self._client._finalizeResponse(
                album,
                Album,
            )
            for album in albums
        ] if albums else None

        if not self.albums:
            album = track.get("album")
            self.albums = [
                self._client._finalizeResponse(
                    album,
                    Album,
                )
            ] if album else None

        timeStamps = track.get("client_timestamps")

        updatedAt = track.get("updated_by_human_at") or (timeStamps.get("updated_by_human_at") if timeStamps else None)
        self.updatedAt = unixToDatetime(updatedAt) if updatedAt else None

        transcribedAt = track.get("transcribedAt")
        self.transcribedAt = unixToDatetime(transcribedAt) if transcribedAt else None

        youtubeUrl = track.get("youtube_url")
        self.youtube = youtubeUrl.replace("http://www.youtube.com/watch?v=", str()) if youtubeUrl else None
        self.startSecond = track.get("youtube_start")
        self.featuredVideo = track.get("featured_video")
        self.soundcloud = track.get("soundcloud_url")
        self.appleMusic = track.get("apple_music_id")
        self.spotify = track.get("spotify_uuid")
        self.vttpId = track.get("vttp_id")

        self.released = track.get("published")
        self.recordingLocation = track.get("recording_location")

        self.hidden = track.get("hidden")
        viewableByRoles = track.get("viewable_by_roles")
        self.viewableByRoles = [
            Role(viewableByRole.replace("_a", "A"))
            for viewableByRole in viewableByRoles
        ] if self.hidden and viewableByRoles else None

        self.number = track.get("number")

        translations = track.get("translation_songs")
        self.translations = [
            self._client._finalizeResponse(
                translation,
                Track,
            )
            for translation in translations
        ] if translations else None

        verifiedContributors = track.get("verified_contributors")
        self.verifiedContributors = [
            self._client._finalizeResponse(
                user,
                User,
            )
            for user in verifiedContributors
        ] if verifiedContributors else None

        verifiedAnnotationsBy = track.get("verified_annotations_by")
        self.verifiedAnnotationsBy = [
            self._client._finalizeResponse(
                user,
                User,
            )
            for user in verifiedAnnotationsBy
        ] if verifiedAnnotationsBy else None

        customRoles = track.get("custom_performances")
        self.customRoles = [
            self._client._finalizeResponse(
                {
                    **artist,
                    **{
                        "role": customRole.get("label"),
                    },
                },
                Artist,
            )
            for customRole in customRoles
            for artist in customRole.get("artists")
        ] if customRoles else None

        stats = track.get("stats")
        if stats:
            self.hot = stats.get("hot")
            views = stats.get("pageviews")
            concurrentCount = stats.get("concurrents")
            contributorCount = stats.get("contributors")
            IQEarnerCount = stats.get("iq_earners")
            transcriberCount = stats.get("transcribers")
            verifiedAnnotationCount = stats.get("verified_annotations")
            acceptedAnnotationCount = stats.get("accepted_annotations")
            unreviewedAnnotationCount = stats.get("unreviewed_annotations")

        else:
            self.hot = None
            views = None
            concurrentCount = None
            contributorCount = None
            IQEarnerCount = None
            transcriberCount = None
            verifiedAnnotationCount = None
            acceptedAnnotationCount = None
            unreviewedAnnotationCount = None

        annotationCount = track.get("annotation_count")
        pyongCount = track.get("pyongs_count")
        commentCount = track.get("comment_count")

        self.stats = self._client._finalizeResponse(
            {
                "views": views,
                "concurrents": concurrentCount,
                "contributors": contributorCount,
                "IQEarners": IQEarnerCount,
                "transcribers": transcriberCount,
                "annotations": annotationCount,
                "verifiedAnnotations": verifiedAnnotationCount,
                "acceptedAnnotations": acceptedAnnotationCount,
                "unreviewedAnnotations": unreviewedAnnotationCount,
                "pyongs": pyongCount,
                "comments": commentCount,
            },
            Stats,
        )

        self.id = track.get("id") or int(track.get("api_path").replace("/songs/", str()))

        self.artistDomain = self.primaryArtist.domain if self.primaryArtist else None
        domain = track.get("path")
        domain = domain[1:-7] if domain else track.get("url").replace("https://genius.com/", str())[:-7]
        self.trackDomain = domain.replace(f"{self.artistDomain}-", str()) if self.artistDomain else None
        self.domain = f"{self.artistDomain}-{self.trackDomain}" if self.artistDomain else domain

        self.url = f'{Genius}{self.domain}-lyrics'

        lyrics = track.get("lyrics")
        self.lyrics = self._client._finalizeResponse(
            {
                **(
                    {
                        "instrumental": track.get("instrumental"),
                        "state": track.get("lyrics_state"),
                        "verified": track.get("lyrics_verified"),
                        "explicit": track.get("explicit"),
                        "music": track.get("music"),
                        "language": track.get("language"),
                        "lyricsPlaceholderReason": track.get("lyrics_placeholder_reason"),
                        "hasInstagramReelAnnotations": track.get("has_instagram_reel_annotations"),
                        "pendingEdits": track.get("pending_lyrics_edits_count"),
                        "verifiedBy": track.get("verified_lyrics_by"),
                        "markedCompleteBy": track.get("lyrics_marked_complete_by"),
                        "staffApprovedBy": track.get("lyrics_marked_staff_approved_by"),
                        "updatedAt": track.get("lyrics_updated_at") or (timeStamps.get("lyrics_updated_at") if timeStamps else None),
                        "ownerId": track.get("lyrics_owner_id"),
                        "track": copy.copy(self),
                    }
                ),
                **(
                    {
                        "plain": lyrics.plain,
                        "markdown": lyrics.markdown,
                        "markdownV2": lyrics.markdownV2,
                        "html": lyrics.html,
                        "instrumental": lyrics.instrumental,
                    }
                    if lyrics and isinstance(lyrics, Lyrics) else dict()
                ),
            },
            Lyrics,
        )

        self.raw = track


    @asyncFunction
    async def get(self, textFormat: TextFormat = None, includeLyrics: bool = False) -> "Track":
        return await self._client.getTrack(self.id, textFormat, includeLyrics)


    @asyncFunction
    async def getLyrics(self, removeSections: bool = False, enhance: bool = True) -> Union[Lyrics, None]:
        return await self._client.getLyrics(removeSections=removeSections, enhance=enhance, track=self)


    @asyncFunction
    async def getAnnotations(self, perPage: int = None, page: int = None, textFormat: TextFormat = None) -> Union[List[Annotation], Annotation, None]:
        return await self._client.getTrackAnnotations(self.id, perPage, page, textFormat)