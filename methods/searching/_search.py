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

from geniux.enums import Sort

class _Search:
    async def _search(self, query: str, path: str, perPage: int = None, page: int = None, sort: Sort = None) -> Union[dict, None]:
        searchResults = await self._req(
            f"search{path}",
            {
                "q": query,
                "per_page": perPage,
                "page": page,
                **({"sort": sort.value}
                if sort else dict()),
            },
        )

        if not searchResults:
            return

        sections = searchResults.get("sections")
        searchResults = sections[0] if sections else searchResults

        return [searchResult.get("result") for searchResult in searchResults.get("hits")] if searchResults else None