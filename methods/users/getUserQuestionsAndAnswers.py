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
from geniux.types import Question, Answer
from geniux.enums import TextFormat

class GetUserQuestionsAndAnswers:
    @asyncFunction
    async def getUserQuestionsAndAnswers(self, id: int, perPage: int = None, page: int = None, textFormat: TextFormat = None) -> Union[List[Union[Question, Answer]], Question, Answer, None]:
        questionsAndAnswers = await self._req(
            f"users/{id}/contributions/questions_and_answers",
            {
                "per_page": perPage,
                "page": page,
                **({"text_format": textFormat.value}
                if textFormat else dict()),
            },
        )

        questionsAndAnswers = questionsAndAnswers.get("contribution_groups")
        if not questionsAndAnswers:
            return

        for idx, QAInfo in enumerate(questionsAndAnswers):
            QA = QAInfo.get("contributions")
            if not QA:
                continue

            QA = QA[0]
            if not QA:
                continue

            questionsAndAnswers[idx] = self._finalizeResponse(QA, Question if QAInfo.get("contribution_type") == "question" else Answer)

        return questionsAndAnswers if len(questionsAndAnswers) != 1 else questionsAndAnswers[0]