import aiohttp

from pathlib import Path


class Unrestrict:
    def __init__(self, rd: any) -> None:
        self.rd = rd

    async def check(self, link: str, password: str = None) -> aiohttp.ClientResponse:
        """Check if a file is downloadable from the hoster

        Args:
            link (str): Original hoster link
            password (str, optional): Password to unlock file from the hoster. Defaults to None.

        Returns:
            aiohttp.ClientResponse: Request object from aiohttp library
        """
        return await self.rd.post("/unrestrict/check", link=link, password=password)

    async def link(self, link: str, password: str = None, remote: str = None) -> aiohttp.ClientResponse:
        """Unrestrict a hoster link and get a new unrestricted link

        Args:
            link (str): Original hoster link
            password (str, optional): Password to unlock file from the hoster. Defaults to None.
            remote (str, optional): 0 or 1, use remote traffic. Defaults to None.

        Returns:
            aiohttp.ClientResponse: Request object from aiohttp library
        """
        return await self.rd.post("/unrestrict/link", link=link, password=password, remote=remote)

    async def folder(self, link: str) -> aiohttp.ClientResponse:
        """Unrestrict a hoster folder link and get individual links

        Args:
            link (str): Original hoster link

        Returns:
            aiohttp.ClientResponse: Request object from aiohttp library (text returns an empty array if no links found)
        """
        return self.rd.post("/unrestrict/folder", link=link)

    async def container_file(self, filepath: Path | str) -> aiohttp.ClientResponse:
        """Decrypt a container file (RSDF, CCF, CCF3, DLC)

        Args:
            filepath (Path | str): Path to container file

        Returns:
            aiohttp.ClientResponse: Request object from aiohttp library
        """
        return await self.rd.put("/unrestrict/containerFile", filepath=filepath)

    async def container_link(self, link: str) -> aiohttp.ClientResponse:
        """Decrypt a container file from a link

        Args:
            link (str): Link to the container file

        Returns:
            aiohttp.ClientResponse: Request object from aiohttp library
        """
        return await self.rd.post("/unrestrict/containerLink", link=link)
