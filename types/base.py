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

from json import JSONEncoder

class Encoder(JSONEncoder):
    def default(self, o) -> any:
        from enum import Enum
        from datetime import datetime, date

        if any((class_.__name__ == "Base" for class_ in o.__class__.__bases__)):
            return o._toDict()

        elif isinstance(o, Enum):
            return o.value

        elif isinstance(o, datetime):
            return o.strftime("%d/%m/%Y %H:%M:%S")

        elif isinstance(o, date):
            return o.strftime("%d/%m/%Y")

        elif isinstance(o, type):
            return o.__name__

        return super().default(o)


class Base:
    def __init__(self, client: "Client") -> None:
        self._client = client


    def _toDict(self) -> dict:
        from types import FunctionType, MethodType

        from geniux.types import Track

        result = dict()
        for key, value in self.__dict__.items():
            if any((value is None, value and (key == "stats" or (isinstance(self, Track) and key == "lyrics")) and sum(1 for key_ in value.__dict__ if value.__dict__[key_] is not None) == (2 if key == "stats" else 4), isinstance(value, (FunctionType, MethodType)), key in ["_client", "raw"])):
                continue

            result[key if not key.startswith("_") else key[1:]] = value

        return result


    def __repr__(self) -> str:
        from json import dumps

        return dumps(self._toDict(), indent=4, ensure_ascii=False, cls=Encoder)