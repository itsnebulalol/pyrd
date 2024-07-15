import aiohttp


class Downloads:
    def __init__(self, rd: any) -> None:
        self.rd = rd

    async def get(self, offset: int = None, page: int = None, limit: int = None) -> aiohttp.ClientResponse:
        """Get user downloads list

        Args:
            offset (int, optional): Starting offset. Defaults to None.
            page (int, optional): Pagination system. Defaults to None.
            limit (int, optional): Entries returned per page / request (must be within 0 and 5000). Defaults to None (100).

        Returns:
            aiohttp.ClientResponse: Request object from aiohttp library
        """
        return await self.rd.get("/downloads", offset=offset, page=page, limit=limit)

    async def delete(self, id: str) -> aiohttp.ClientResponse:
        """Delete a link from downloads list

        Args:
            id (str): Torrent id from /downloads or /unrestrict/link

        Returns:
            aiohttp.ClientResponse: Request object from aiohttp library
        """
        return await self.rd.delete(f"/downloads/delete/{id}")
