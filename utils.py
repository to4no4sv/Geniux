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

import re
from typing import Union, List
from datetime import datetime

def unixToDatetime(seconds: int) -> datetime:
    return datetime.utcfromtimestamp(seconds)


def addHTTPsToUrl(url: str) -> str:
    if not ("https://" in url or "http://" in url):
        url = "https://" + url

    return url


def parsePhoto(photo: Union[str, None]) -> Union[str, None]:
    return (photo if "?" not in photo else photo[:photo.rfind("?")]) if photo else None


def artistsToStr(mainArtist: Union["Artist", None] = None, featuredArtists: Union[List["Artist"], None] = None) -> Union[str, None]:
    if not mainArtist:
        return

    artist = (", ".join([mainArtist.nickname]) +
    ((" feat. " + ((", ".join([artist.nickname for artist in featuredArtists[:-1]]) + " & " + featuredArtists[-1].nickname) if len(featuredArtists) > 1 else featuredArtists[0].nickname)) if featuredArtists else str()))

    return artist


def clean(string: Union[str, None]) -> Union[str, None]:
    if not string:
        return

    return string.strip().replace("​", str()).replace("\\xa0", " ").replace("’", "'")


russianLetters = set("абвгдеёжзийклмнопрстуфхцчшщъыьэюя")

def cleanTitle(title: Union[str, None]) -> Union[str, None]:
    if not title:
        return

    if "(" in title:
        if any(char.isalpha() and char.lower() in russianLetters for char in title[:title.find("(")]):
            titlePartToCheck = title[title.find("(") + 1: title.find(")")].lower()

            if any(char.isalpha() and char.lower() in russianLetters for char in titlePartToCheck):
                if any(substring in titlePartToCheck for substring in ["freestyle", "spedup", "sped up", "speedup", "speed up", "slowed", "reverb", "leak", "remix", "cover", "bonus"]) or any(char.isalpha() and char.lower() in russianLetters for char in titlePartToCheck):
                    title = title[:title.find(")") + 1]

                else:
                    title = title[:title.rfind(" (")]

            else:
                title = title[:title.rfind(" (")]

    return clean(title)


def cleanArtists(artists: Union[str, None]) -> Union[str, None]:
    if not artists:
        return

    if " & " in artists:
        artists = artists.split(" & ", 1)
        artists = artists[0].split(", ") + [artists[1]]

    if not isinstance(artists, list):
        artists = [artists]

    for idx, artist in enumerate(artists):
        artist = re.sub(r"\s*\((rus|ru|ukr|uk|prod|producer|0|1|2|3)\)", str(), artist, flags=re.IGNORECASE)
        if "(" in artist:
            if any(char.isalpha() and char.lower() in russianLetters for char in artist[:artist.find("(")]):
                nicknamePartToCheck = artist[artist.find("(") + 1: artist.find(")")].lower()

                if any(char.isalpha() and char.lower() in russianLetters for char in nicknamePartToCheck):
                    artist = artist[:artist.find(")") + 1]

                else:
                    artist = artist[:artist.rfind(" (")]

        artists[idx] = artist

    return clean(", ".join([artist for artist in artists[:-1]]) + " & " + artists[-1] if len(artists) > 1 else artists[0])