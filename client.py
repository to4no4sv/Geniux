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

from httpx import AsyncClient
from typing import Union, List, Type, Any

from geniux.aio import asyncFunction
from geniux.config import GeniusAPI
from geniux.errors import *

from geniux.webClient import Client as WebClient

from geniux.methods import *
from geniux.enums import Language

class Client(
    Searching,
    Artists,
    Albums,
    Tracks,
    Annotations,
    Users,
    Charts,
):
    """
    Класс для взаимодействия с Genius.

    Аргументы:
        token (str, optional): Токен доступа к Genius API. Требуется для некоторых методов.\n
        language (Language, optional): Язык ошибок (например, `Language.Russian` для русского, `Language.English` для английского). Если не указан, используются все языки.\n
        proxies (dict, optional): прокси, которые будут использоваться при запросах. Формат {"протокол": "логин:пароль@IP:порт"}\n

    Пример использования:
        from geniux.enums import Language
        client = Client(token="yourToken", language=Language.Russian, proxies={"http": "IP:port", "socks5": "login:password@IP:port"})
        result = client.searchTracks("New Sylveon")
        print(result)
    """


    def __init__(self, token: str = None, language: Language = None, proxies: dict = None) -> None:
        self._token = token
        self._language = language if language and isinstance(language, Language) else None

        if not proxies:
            self._proxies = None

        else:
            if not isinstance(proxies, dict):
                self._raiseError("invalidProxyType")

            newProxies = dict()

            for scheme in proxies.keys():
                if scheme.lower() not in ("http", "https", "socks4", "socks5"):
                    self._raiseError("invalidProxyDict")

                proxyURL = proxies.get(scheme)
                scheme = scheme.lower() + ("://" if not scheme.endswith("://") else str())
                newProxies[scheme] = (scheme if "://" not in proxyURL else str()) + proxyURL

            self._proxies = newProxies

        import sys
        if sys.version_info < (3, 6):
            ruWarning = "Внимание: Работоспособость этой библиотеки гарантируется только при Python 3.6 или выше. Вы используете версию {}."
            enWarning = "Attention: The functionality of this library is guaranteed only for Python 3.6 or higher. You are using version {}."

            from warnings import warn
            warn(
                (ruWarning if self._language == Language.Russian else (enWarning if self._language == Language.English else "🇷🇺: " + ruWarning + " 🇬🇧: " + enWarning)).format(str(sys.version_info.major) + "." + str(sys.version_info.minor)),
                UserWarning
            )

        self._proxySession = AsyncClient(proxies=self._proxies)
        self._proxyClient = WebClient(self._proxySession)

        self._session = AsyncClient(proxies=None)
        self._client = WebClient(self._session)

        self._closed = False

        try:
            asyncio.get_running_loop()

        except RuntimeError:
            from .version import __version__
            from packaging import version

            latestVersion = self._client.req("https://pypi.org/pypi/geniux/json").get("info").get("version")

            if version.parse(latestVersion) > version.parse(__version__):
                ruWarning = f"Внимание: Доступна новая версия библиотеки {latestVersion} (https://pypi.org/project/geniux). Вы используете версию {__version__}."
                enWarning = f"Attention: A new version of the library {latestVersion} (https://pypi.org/project/geniux) is available. You are using version {__version__}."

                from warnings import warn
                warn(
                    ruWarning if self._language == Language.Russian else (enWarning if self._language == Language.English else "🇷🇺: " + ruWarning + " 🇬🇧: " + enWarning),
                    UserWarning
                )


    async def checkUpdates(self) -> None:
        if self._closed:
            self._raiseError("sessionClosed")

        from .version import __version__
        from packaging import version

        latestVersion = (await self._client.req("https://pypi.org/pypi/geniux/json")).get("info").get("version")

        if version.parse(latestVersion) > version.parse(__version__):
            ruWarning = f"Внимание: Доступна новая версия библиотеки {latestVersion} (https://pypi.org/project/geniux). Вы используете версию {__version__}."
            enWarning = f"Attention: A new version of the library {latestVersion} (https://pypi.org/project/geniux) is available. You are using version {__version__}."

            from warnings import warn
            warn(
                ruWarning if self._language == Language.Russian else (enWarning if self._language == Language.English else "🇷🇺: " + ruWarning + " 🇬🇧: " + enWarning),
                UserWarning
            )


    def __enter__(self) -> "Client":
        return self


    async def __aenter__(self) -> "Client":
        return self


    def __exit__(self, exc_type, exc_value, traceback) -> None:
        try:
            self.close()

        except SessionAlreadyClosed:
            pass


    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        try:
            await self.close()

        except SessionAlreadyClosed:
            pass


    @asyncFunction
    async def close(self) -> None:
        """
        Закрывает текующую сессию. Для отправки новых запросов потребуется создать новый объект класса `Client` или использовать метод `reconnect`.
        """

        if self._closed:
            self._raiseError("sessionAlreadyClosed")
            return

        self._closed = True
        await self._session.aclose()
        await self._proxySession.aclose()


    @asyncFunction
    async def reconnect(self) -> None:
        """
        Пересоздаёт закрытую сессию.
        """

        if not self._closed:
            self._raiseError("sessionAlreadyOpened")
            return

        self._closed = False
        self._proxySession = AsyncClient(proxies=self._proxies)
        self._proxyClient = WebClient(self._proxySession)
        self._session = AsyncClient(proxies=None)
        self._client = WebClient(self._session)


    async def _req(self, method: str, params: dict = None, HTTPMethod: str = "GET") -> Union[dict, None]:
        if self._closed:
            self._raiseError("sessionClosed")

        if not params:
            params = dict()

        else:
            params = {k: v for k, v in params.items() if v is not None}

        fullParams = {
            **params,
            **(
                {
                    "Authorization": f"Bearer {self._token}",
                }
                if self._token else dict()
            ),
        }

        req = await self._proxyClient.req(f"{GeniusAPI}{method}", fullParams, method=HTTPMethod)

        error = req.get("error") if isinstance(req, dict) else None
        if error:
            return error

        if isinstance(req, list) and len(req) == 1:
            req = req[0]

        return req


    def _raiseError(self, errorType: Union[str, None]) -> None:
        if not errorType:
            return

        errorsDict = {
            "unknown": Unknown,

            "sessionClosed": SessionClosed,
            "sessionAlreadyClosed": SessionAlreadyClosed,
            "sessionAlreadyOpened": SessionAlreadyOpened,

            "GeniusInvalidToken": GeniusInvalidToken,

            "invalidMethod": InvalidMethod,
            "accessDenied": AccessDenied,

            "noneQuery": NoneQuery,

            "needsTrackIdOrTrackParameter": NeedsTrackIdOrTrackParameter,
            "needsTrackIdOrTrackParameterNotBoth": NeedsTrackIdOrTrackParameterNotBoth,

            "tooHighRequestSendingRate": TooHighRequestSendingRate,

            "invalidProxyType": InvalidProxyType,
            "invalidProxyDict": InvalidProxyDict,
        }

        if errorType not in errorsDict:
            errorType = "unknown"

        error = errorsDict.get(errorType)()

        if self._language:
            if self._language == Language.Russian:
                languageAttr = "ru"

            elif self._language == Language.English:
                languageAttr = "en"

            for attr in ["ru", "en"]:
                if attr != languageAttr:
                    delattr(error, attr)

        raise error


    def _finalizeResponse(self, response: Union[List[dict], dict], objectType: Type[Any]) -> Union[List[Any], None]:
        if not (response or response is False):
            return

        response = [objectType(obj, client=self) for obj in (response if isinstance(response, list) else [response])]

        return response if len(response) > 1 else response[0]