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
from typing import Union, List

from geniux.aio import asyncFunction
from geniux.types import Annotation
from geniux.enums import Sort, TextFormat

class GetUserAnnotations:
    @asyncFunction
    async def getUserAnnotations(self, id: int, perPage: int = None, page: int = None, sort: Sort = None, textFormat: TextFormat = None) -> Union[List[Annotation], Annotation, None]:
        annotations = await self._req(
            f"users/{id}/contributions/annotations",
            {
                "per_page": perPage,
                "page": page,
                **({"sort": sort.value}
                if sort else dict()),
                **({"text_format": textFormat.value}
                if textFormat else dict()),
            },
        )

        annotations = annotations.get("contribution_groups")
        if not annotations:
            return

        for idx, annotationInfo in enumerate(annotations):
            annotation = annotationInfo.get("contributions")
            if not annotation:
                continue

            annotation = annotation[0]
            if not annotation:
                continue

            annotations[idx] = annotation

        return self._finalizeResponse(annotations, Annotation)