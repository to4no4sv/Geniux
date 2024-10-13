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

from .artist import Artist
from .album import Album
from .coverArt import CoverArt
from .annotation import Annotation
from .track import Track
from .lyrics import Lyrics
from .genre import Genre
from .user import User
from .comment import Comment
from .pyong import Pyong
from .question import Question
from .answer import Answer

"""from . import *
import os
import importlib
import inspect

classes = dict()

folderPath = os.path.dirname(__file__)

for filename in os.listdir(folderPath):
    if filename.endswith(".py") and filename != "__init__.py":
        moduleName = f".{filename[:-3]}"
        module = importlib.import_module(moduleName, package=__package__)

        expectedClassName = filename[:-3].capitalize()

        for name, obj in inspect.getmembers(module):
            if inspect.isclass(obj) and name == expectedClassName:
                classes[name] = obj

__all__ = list(classes.keys())
globals().update(classes)"""