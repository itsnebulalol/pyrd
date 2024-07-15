import aiohttp

from pathlib import Path

from . import exceptions, data
from .endpoints import *


class RealDebrid:
    def __init__(self, token: str, base_url: str = "https://api.real-debrid.com/rest/1.0") -> None:
        self.token = token
        self.base_url = base_url
        self.session = aiohttp.ClientSession(headers={"Authorization": f"Bearer {self.token}"})

        self.validate_token()

        self.system = System(self)
        self.user = User(self)
        self.unrestrict = Unrestrict(self)
        self.traffic = Traffic(self)
        self.streaming = Streaming(self)
        self.downloads = Downloads(self)
        self.torrents = Torrents(self)
        self.hosts = Hosts(self)
        self.settings = Settings(self)

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        await self.close()

    def validate_token(self) -> None:
        """Validate if self.token is not empty

        Raises:
            exceptions.InvalidTokenException: Thrown if validation failed
        """
        if self.token in (None, ""):
            raise exceptions.InvalidTokenException()

    async def get(self, path: str, **options) -> aiohttp.ClientResponse:
        """Make an HTTP GET request to the Real-Debrid API

        Args:
            path (str): API path

        Returns:
            aiohttp.ClientResponse: Request object from aiohttp library
        """
        async with self.session.get(
            self.base_url + path, params={k: v for k, v in options.items() if v is not None}
        ) as req:
            return await self.handler(req, path)

    async def post(self, path: str, **payload) -> aiohttp.ClientResponse:
        """Make an HTTP POST request to the Real-Debrid API

        Args:
            path (str): API path

        Returns:
            aiohttp.ClientResponse: Request object from aiohttp library
        """
        async with self.session.post(self.base_url + path, data=payload) as req:
            return await self.handler(req, path)

    async def put(self, path: str, filepath: Path | str, **payload) -> aiohttp.ClientResponse:
        """Make an HTTP PUT request to the Real-Debrid API

        Args:
            path (str): API path
            filepath (Path | str): Path to a file

        Returns:
            aiohttp.ClientResponse: Request object from aiohttp library
        """
        with open(filepath, "rb") as file:
            async with self.session.put(
                self.base_url + path, data=file, params={k: v for k, v in payload.items() if v is not None}
            ) as req:
                return await self.handler(req, path)

    async def delete(self, path: str) -> aiohttp.ClientResponse:
        """Make an HTTP DELETE request to the Real-Debrid API

        Args:
            path (str): API path

        Returns:
            aiohttp.ClientResponse: Request object from aiohttp library
        """
        async with self.session.delete(self.base_url + path) as req:
            return await self.handler(req, path)

    async def handler(self, req: aiohttp.ClientResponse, path: str) -> aiohttp.ClientResponse:
        """API request handler

        Args:
            req (aiohttp.ClientResponse): Finished request
            path (str): API path

        Raises:
            exceptions.APIError: Thrown when an HTTP error is caught
            exceptions.RealDebridError: Thrown when an error returned from Real-Debrid is caught

        Returns:
            aiohttp.ClientResponse: Request object from aiohttp library
        """
        try:
            req.raise_for_status()
        except aiohttp.ClientError as e:
            raise exceptions.APIError(e)

        json = await req.json()
        if "error_code" in json:
            code = json["error_code"]
            message = data.error_codes.get(str(code), "Unknown error")
            raise exceptions.RealDebridError(f"{code}: {message} at {path}")

        return req

    async def close(self) -> None:
        await self.session.close()
