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
from geniux.types import Annotation, Track, Comment, Pyong, Question, Answer
from geniux.enums import Sort, TextFormat

class GetUserActivities:
    @asyncFunction
    async def getUserActivities(self, id: int, perPage: int = None, page: int = None, sort: Sort = None, textFormat: TextFormat = None) -> Union[List[Union[Annotation, Track, Question, Answer, Comment, Pyong]], Annotation, Track, Question, Answer, Comment, Pyong, None]:
        activities = await self._req(
            f"users/{id}/contributions",
            {
                "per_page": perPage,
                "page": page,
                **({"sort": sort.value}
                if sort else dict()),
                **({"text_format": textFormat.value}
                if textFormat else dict()),
            },
        )

        activities = activities.get("contribution_groups")
        if not activities:
            return

        for idx, activityInfo in enumerate(activities):
            activity = activityInfo.get("contributions")
            if not activity:
                continue

            activity = activity[0]
            if not activity:
                continue

            activityType = activityInfo.get("contribution_type")
            activityType = Track if activityType == "song" else (Annotation if activityType == "annotation" else (Comment if activityType == "comment" else (Pyong if activityType == "pyong" else (Question if activityType == "question" else (Answer if activityType == "answer" else ...)))))

            if activityType is Track:
                activity["transcribedAt"] = activityInfo.get("date")

            activities[idx] = self._finalizeResponse(activity, activityType)

        return activities if len(activities) != 1 else activities[0]