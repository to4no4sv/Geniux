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

import asyncio
import re
from typing import Union
from bs4 import BeautifulSoup

from geniux.aio import asyncFunction
from geniux.config import Genius
from geniux.utils import clean
from geniux.types import Track, Lyrics

class GetLyrics:
    @asyncFunction
    async def getLyrics(self, trackId: int = None, removeSections: bool = False, enhance: bool = True, track: Track = None) -> Union[Lyrics, None]:
        if not any((trackId, track)):
            self._raiseError("needsTrackIdOrTrackParameter")

        elif all((trackId, track)):
            self._raiseError("needsTrackIdOrTrackParameterNotBoth")

        url = f"{Genius}songs/{trackId}" if not track or not track.url else f"{track.url}?bagon=1"
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:126.0) Gecko/20100101 Firefox/126.0",
        }

        response = await self._client.req(url, headers=headers, responseType="response")
        if response.status_code == 301:
            response = await self._client.req(f'{response.headers.get("Location")}?bagon=1', headers=headers, responseType="response")

        if response.status_code == 302:
            response = await self._proxyClient.req(url, headers=headers, responseType="response")
            if response.status_code == 302:
                self._raiseError("trackNotAvailableInYourCountry")

        if response.status_code == 404:
            return

        text = re.sub(r"<br/>", "\n", response.text)

        soup = BeautifulSoup(text, "html.parser")
        div = soup.find("div", class_=re.compile("^lyrics$|Lyrics__Root"))
        if div is None:
            return None

        lyricsContent = div.extract()

        pattern = re.compile(r"^(Pyong|LyricsFooter|LyricsHeader)__Container")
        for div in lyricsContent.find_all("div", class_=pattern):
            div.decompose()

        adClassesPattern = re.compile(r"(DfpAd__Container|SidebarAd__Container|SidebarAd__StickyContainer|RightSidebar__Container|InreadContainer__Container)")
        for adBlock in lyricsContent.find_all(class_=adClassesPattern):
            adBlock.replace_with(str())

        for keyword in ["You might also like", "Embed"]:
            for block in lyricsContent.find_all(string=re.compile(keyword)):
                block.parent.replace_with(str())

        pattern = re.compile(r"^Lyrics__Container")
        for container in lyricsContent.find_all("div", class_=pattern):
            container.insert_before("\n")
            container.unwrap()

        lyricsContent = str(lyricsContent)
        lyricsContent = lyricsContent.replace("  ", " ")
        lyricsContent = re.sub(r'<a class="ReferentFragmentdesktop__ClickTarget.*?" href=".*?(/|.*?)"><span class="ReferentFragmentdesktop__Highlight.*?">(.*?)</span></a>', r"\2", lyricsContent, flags=re.DOTALL)
        lyricsContent = re.sub(r'<span style=".*".*></span>', str(), lyricsContent)
        lyricsContent = lyricsContent[lyricsContent.find(">") + 2:lyricsContent.rfind("</div>")]

        lyricsHTML = clean(lyricsContent)
        instrumental = '<div class="LyricsPlaceholder__Message-uen8er-2 gotKKY">This song is an instrumental</div>' in lyricsHTML
        if not instrumental:
            if enhance:
                lyricsHTML = lyricsHTML.replace("\n\n\n", "\n\n")

                lines = lyricsHTML.split("\n")
                if lines and len(lines) >= 2 and "текст песни" in lines[0].lower() and not lines[1].strip():
                    for _ in range(2):
                        lines.pop(0)

                lyricsHTML = "\n".join(lines)

            if removeSections:
                pattern = r"(?:\n\n|\A)\[[^\[\]\?]+\]\n"
                lyricsHTML = re.sub(pattern, lambda match: "\n\n" if match.start() != 0 else str(), lyricsHTML)

            lyricsMarkdown = re.sub(r"([_*~`#+|{}\\])", r"\\\1", lyricsHTML)
            lyricsMarkdown = re.sub(r"<b>(.*?)</b>", r"**\1**", lyricsMarkdown, flags=re.DOTALL)

            lyricsMarkdownV1 = re.sub(r"<i>(.*?)</i>", r"*\1*", lyricsMarkdown, flags=re.DOTALL)
            lyricsMarkdownV2 = re.sub(r"<i>(.*?)</i>", r"__\1__", lyricsMarkdown, flags=re.DOTALL)
            #lyricsMarkdownV1 = re.sub(r">", r"\\>", lyricsMarkdownV1)
            #lyricsMarkdownV2 = re.sub(r">", r"\\>", lyricsMarkdownV2)

            lyricsPlain = BeautifulSoup(lyricsHTML, "html.parser").get_text()

        lyrics = self._finalizeResponse(
            {
                **(
                    {
                        "plain": lyricsPlain,
                        "markdown": lyricsMarkdownV1,
                        "markdownV2": lyricsMarkdownV2,
                        "html": lyricsHTML,
                    }
                    if not instrumental else dict()
                ),
                "instrumental": instrumental,
                "track": track,
            },
            Lyrics,
        )

        return lyrics
