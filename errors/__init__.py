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

from .error import Error
from .unknown import Unknown

from .sessionClosed import SessionClosed
from .sessionAlreadyClosed import SessionAlreadyClosed
from .sessionAlreadyOpened import SessionAlreadyOpened

from .geniusInvalidToken import GeniusInvalidToken

from .invalidMethod import InvalidMethod
from .accessDenied import AccessDenied

from .noneQuery import NoneQuery

from .needsTrackIdOrTrackParameter import NeedsTrackIdOrTrackParameter
from .needsTrackIdOrTrackParameterNotBoth import NeedsTrackIdOrTrackParameterNotBoth

from .tooHighRequestSendingRate import TooHighRequestSendingRate

from .invalidProxyType import InvalidProxyType
from .invalidProxyDict import InvalidProxyDict