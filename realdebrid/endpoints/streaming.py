import aiohttp


class Streaming:
    def __init__(self, rd: any) -> None:
        self.rd = rd

    async def transcode(self, id: str) -> aiohttp.ClientResponse:
        """Get transcoding links for given file

        Args:
            id (str): Torrent id from /downloads or /unrestrict/link

        Returns:
            aiohttp.ClientResponse: Request object from aiohttp library
        """
        return await self.rd.get(f"/streaming/transcode/{id}")

    async def media_infos(self, id: str) -> aiohttp.ClientResponse:
        """Get detailled media informations for given file

        Args:
            id (str): Torrent id from /downloads or /unrestrict/link

        Returns:
            aiohttp.ClientResponse: Request object from aiohttp library
        """
        return await self.rd.get(f"/streaming/mediaInfos/{id}")
