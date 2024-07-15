import aiohttp


class User:
    def __init__(self, rd: any) -> None:
        self.rd = rd

    async def get(self) -> aiohttp.ClientResponse:
        """Returns some information on the current user

        Returns:
            aiohttp.ClientResponse: Request object from aiohttp library
        """
        return await self.rd.get("/user")
