import aiohttp


class Hosts:
    def __init__(self, rd: any) -> None:
        self.rd = rd

    async def get(self) -> aiohttp.ClientResponse:
        """Get supported hosts

        Returns:
            aiohttp.ClientResponse: Request object from aiohttp library
        """
        return await self.rd.get("/hosts")

    async def status(self) -> aiohttp.ClientResponse:
        """Get status of supported hosters, and from competetors

        Returns:
            aiohttp.ClientResponse: Request object from aiohttp library
        """
        return await self.rd.get("/hosts/status")

    async def regex(self) -> aiohttp.ClientResponse:
        """Get all supported links regex

        Returns:
            aiohttp.ClientResponse: Request object from aiohttp library
        """
        return await self.rd.get("/hosts/regex")

    async def regex_folder(self) -> aiohttp.ClientResponse:
        """Get all supported folder regex

        Returns:
            aiohttp.ClientResponse: Request object from aiohttp library
        """
        return await self.rd.get("/hosts/regexFolder")

    async def domains(self) -> aiohttp.ClientResponse:
        """Get all supported hoster domains

        Returns:
            aiohttp.ClientResponse: Request object from aiohttp library
        """
        return await self.rd.get("/hosts/domains")
