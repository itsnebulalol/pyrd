import aiohttp

from pathlib import Path

from . import exceptions, data


class RealDebrid:
    def __init__(self, token: str, base_url: str = "https://api.real-debrid.com/rest/1.0") -> None:
        self.token = token
        self.base_url = base_url
        self.session = aiohttp.ClientSession(headers={"Authorization": f"Bearer {self.token}"})

        self.validate_token()

        self.system = self.System(self)
        self.user = self.User(self)
        self.unrestrict = self.Unrestrict(self)
        self.traffic = self.Traffic(self)
        self.streaming = self.Streaming(self)
        self.downloads = self.Downloads(self)
        self.torrents = self.Torrents(self)
        self.hosts = self.Hosts(self)
        self.settings = self.Settings(self)

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

    class User:
        def __init__(self, rd: any) -> None:
            self.rd = rd

        async def get(self) -> aiohttp.ClientResponse:
            """Returns some information on the current user

            Returns:
                aiohttp.ClientResponse: Request object from aiohttp library
            """
            return await self.rd.get("/user")

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

    class Settings:
        def __init__(self, rd: any) -> None:
            self.rd = rd

        async def get(self) -> aiohttp.ClientResponse:
            """Get current user settings with possible values to update

            Returns:
                aiohttp.ClientResponse: Request object from aiohttp library
            """
            return await self.rd.get("/settings")

        async def update(self, setting_name: str, setting_value: str) -> aiohttp.ClientResponse:
            """Update a user setting

            Args:
                setting_name (str): Setting name
                setting_value (str): Setting value

            Returns:
                aiohttp.ClientResponse: Request object from aiohttp library
            """
            return await self.rd.post("/settings/update", setting_name=setting_name, setting_value=setting_value)

        async def convert_points(self) -> aiohttp.ClientResponse:
            """Convert fidelity points

            Returns:
                aiohttp.ClientResponse: Request object from aiohttp library
            """
            return await self.rd.post("/settings/convertPoints")

        async def change_password(self) -> aiohttp.ClientResponse:
            """Send the verification email to change the account password

            Returns:
                aiohttp.ClientResponse: Request object from aiohttp library
            """
            return await self.rd.post("/settings/changePassword")

        async def avatar_file(self, filepath: Path | str) -> aiohttp.ClientResponse:
            """Upload a new user avatar image

            Args:
                filepath (Path | str): Path to the avatar url

            Returns:
                aiohttp.ClientResponse: Request object from aiohttp library
            """
            return await self.rd.put("/settings/avatarFile", filepath=filepath)

        async def avatar_delete(self) -> aiohttp.ClientResponse:
            """Reset user avatar image to default

            Returns:
                aiohttp.ClientResponse: Request object from aiohttp library
            """
            return await self.rd.delete("/settings/avatarDelete")
