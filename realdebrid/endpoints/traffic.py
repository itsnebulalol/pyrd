import aiohttp


class Traffic:
    def __init__(self, rd: any) -> None:
        self.rd = rd

    async def get(self) -> aiohttp.ClientResponse:
        """Get traffic information for limited hosters

        Returns:
            aiohttp.ClientResponse: Request object from aiohttp library
        """
        return await self.rd.get("/traffic")

    async def details(self, start: str = None, end: str = None) -> aiohttp.ClientResponse:
        """Get traffic details on each hoster during a defined period

        Args:
            start (str, optional): Start date (YYYY-MM-DD). Defaults to None (a week ago).
            end (str, optional): End date (YYYY-MM-DD). Defaults to None (today).

        Returns:
            aiohttp.ClientResponse: Request object from aiohttp library
        """
        return await self.rd.get("/traffic/details", start=start, end=end)
