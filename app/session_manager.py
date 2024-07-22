import aiohttp

class SessionManager:
    def __init__(self):
        self._session = None

    async def init(self):
        if self._session is None:
            self._session = aiohttp.ClientSession()

    async def close(self):
        if self._session and not self._session.closed:
            await self._session.close()

    @property
    def session(self):
        return self._session
