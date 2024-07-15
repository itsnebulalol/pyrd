import aiohttp


class System:
    def __init__(self, rd: any) -> None:
        self.rd = rd

    async def disable_token(self) -> aiohttp.ClientResponse:
        """Disable current access token

        Returns:
            aiohttp.ClientResponse: Request object from aiohttp library
        """
        return await self.rd.get("/disable_access_token")

    async def time(self) -> aiohttp.ClientResponse:
        """Get server time

        Returns:
            aiohttp.ClientResponse: Request object from aiohttp library
        """
        return await self.rd.get("/time")

    async def iso_time(self) -> aiohttp.ClientResponse:
        """Get server time in ISO

        Returns:
            aiohttp.ClientResponse: Request object from aiohttp library
        """
        return await self.rd.get("/time/iso")
