import aiohttp

from pathlib import Path


class Torrents:
    def __init__(self, rd: any) -> None:
        self.rd = rd

    async def get(
        self, offset: int = None, page: int = None, limit: int = None, filter: str = None
    ) -> aiohttp.ClientResponse:
        """Get user torrents list

        Args:
            offset (int, optional): Starting offset. Defaults to None.
            page (int, optional): Pagination system. Defaults to None.
            limit (int, optional): Entries returned per page / request (must be within 0 and 5000). Defaults to None (100).
            filter (str, optional): "active", list active torrents only. Defaults to None.

        Returns:
            aiohttp.ClientResponse: Request object from aiohttp library
        """
        return await self.rd.get("/torrents", offset=offset, page=page, limit=limit, filter=filter)

    async def info(self, id: str) -> aiohttp.ClientResponse:
        """Get information of a torrent

        Args:
            id (str): Torrent id from /downloads or /unrestrict/link

        Returns:
            aiohttp.ClientResponse: Request object from aiohttp library
        """
        return await self.rd.get(f"/torrents/info/{id}")

    async def instant_availability(self, hash: str) -> aiohttp.ClientResponse:
        """Get list of instantly available file IDs by hoster

        Args:
            hash (str): SHA1 of the torrent

        Returns:
            aiohttp.ClientResponse: Request object from aiohttp library
        """
        return await self.rd.get(f"/torrents/instantAvailability/{hash}")

    async def active_count(self) -> aiohttp.ClientResponse:
        """Get currently active torrents number and the current maximum limit

        Returns:
            aiohttp.ClientResponse: Request object from aiohttp library
        """
        return await self.rd.get("/torrents/activeCount")

    async def available_hosts(self) -> aiohttp.ClientResponse:
        """Get available hosts to upload the torrent to

        Returns:
            aiohttp.ClientResponse: Request object from aiohttp library
        """
        return await self.rd.get("/torrents/availableHosts")

    async def add_torrent(self, filepath: Path | str, host: str = None) -> aiohttp.ClientResponse:
        """Add a torrent file to download

        Args:
            filepath (Path | str): Path to torrent file
            host (str, optional): Hoster domain (from torrents.available_hosts). Defaults to None.

        Returns:
            aiohttp.ClientResponse: Request object from aiohttp library
        """
        return await self.rd.put("/torrents/addTorrent", filepath=filepath, host=host)

    async def add_magnet(self, magnet: str, host: str = None) -> aiohttp.ClientResponse:
        """Add a magnet link to download

        Args:
            magnet (str): Manget link
            host (str, optional): Hoster domain (from torrents.available_hosts). Defaults to None.

        Returns:
            aiohttp.ClientResponse: Request object from aiohttp library
        """
        return await self.rd.post("/torrents/addMagnet", magnet=f"magnet:?xt=urn:btih:{magnet}", host=host)

    async def select_files(self, id: str, files: str) -> aiohttp.ClientResponse:
        """Select files of a torrent to start it

        Args:
            id (str): Torrent id from /downloads or /unrestrict/link
            files (str): Selected files IDs (comma separated) or "all"

        Returns:
            aiohttp.ClientResponse: Request object from aiohttp library
        """
        return await self.rd.post(f"/torrents/selectFiles/{id}", files=files)

    async def delete(self, id: str) -> aiohttp.ClientResponse:
        """Delete a torrent from torrents list

        Args:
            id (str): Torrent id from /downloads or /unrestrict/link

        Returns:
            aiohttp.ClientResponse: Request object from aiohttp library
        """
        return await self.rd.delete(f"/torrents/delete/{id}")
