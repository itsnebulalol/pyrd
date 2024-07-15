import requests

from pathlib import Path

from . import exceptions, data


class RealDebrid:
    def __init__(self, token: str, base_url: str = "https://api.real-debrid.com/rest/1.0") -> None:
        self.token = token
        self.base_url = base_url
        self.headers = {"Authorization": f"Bearer {self.token}"}

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

    def validate_token(self) -> None:
        """Validate if self.token is not empty

        Raises:
            exceptions.InvalidTokenException: Thrown if validation failed
        """
        if self.token in (None, ""):
            raise exceptions.InvalidTokenException()

    def get(self, path: str, **options) -> requests.Response:
        """Make an HTTP GET request to the Real-Debrid API

        Args:
            path (str): API path

        Returns:
            requests.Response: Request object from requests library
        """
        req = requests.get(self.base_url + path, headers=self.headers, params=options)
        return self.handler(req, path)

    def post(self, path: str, **payload) -> requests.Response:
        """Make an HTTP POST request to the Real-Debrid API

        Args:
            path (str): API path

        Returns:
            requests.Response: Request object from requests library
        """
        req = requests.post(self.base_url + path, headers=self.headers, data=payload)
        return self.handler(req, path)

    def put(self, path: str, filepath: Path | str, **payload) -> requests.Response:
        """Make an HTTP PUT request to the Real-Debrid API

        Args:
            path (str): API path
            filepath (Path | str): Path to a file

        Returns:
            requests.Response: Request object from requests library
        """
        with open(filepath, "rb") as file:
            req = requests.put(self.base_url + path, headers=self.headers, data=file, params=payload)
        return self.handler(req, path)

    def delete(self, path: str) -> requests.Response:
        """Make an HTTP DELETE request to the Real-Debrid API

        Args:
            path (str): API path

        Returns:
            requests.Response: Request object from requests library
        """
        req = requests.delete(self.base_url + path, headers=self.headers)
        return self.handler(req, path)

    def handler(self, req: requests.Response, path: str) -> requests.Response:
        """API request handler

        Args:
            req (requests.Response): Finished request
            path (str): API path

        Raises:
            exceptions.APIError: Thrown when an HTTP error is caught
            exceptions.RealDebridError: Thrown when an error returned from Real-Debrid is caught

        Returns:
            requests.Response: Request object from requests library
        """
        try:
            req.raise_for_status()
        except (
            requests.exceptions.HTTPError,
            requests.exceptions.ConnectionError,
            requests.exceptions.Timeout,
            requests.exceptions.RequestException,
        ) as e:
            raise exceptions.APIError(e)

        if "error_code" in req.json():
            code = req.json()["error_code"]
            message = data.error_codes.get(str(code), "Unknown error")
            raise exceptions.RealDebridError(f"{code}: {message} at {path}")

        return req

    class System:
        def __init__(self, rd: any) -> None:
            self.rd = rd

        def disable_token(self) -> requests.Response:
            """Disable current access token

            Returns:
                requests.Response: Request object from requests library
            """
            return self.rd.get("/disable_access_token")

        def time(self) -> requests.Response:
            """Get server time

            Returns:
                requests.Response: Request object from requests library
            """
            return self.rd.get("/time")

        def iso_time(self) -> requests.Response:
            """Get server time in ISO

            Returns:
                requests.Response: Request object from requests library
            """
            return self.rd.get("/time/iso")

    class User:
        def __init__(self, rd: any) -> None:
            self.rd = rd

        def get(self) -> requests.Response:
            """Returns some information on the current user

            Returns:
                requests.Response: Request object from requests library
            """
            return self.rd.get("/user")

    class Unrestrict:
        def __init__(self, rd: any) -> None:
            self.rd = rd

        def check(self, link: str, password: str = None) -> requests.Response:
            """Check if a file is downloadable from the hoster

            Args:
                link (str): Original hoster link
                password (str, optional): Password to unlock file from the hoster. Defaults to None.

            Returns:
                requests.Response: Request object from requests library
            """
            return self.rd.post("/unrestrict/check", link=link, password=password)

        def link(self, link: str, password: str = None, remote: str = None) -> requests.Response:
            """Unrestrict a hoster link and get a new unrestricted link

            Args:
                link (str): Original hoster link
                password (str, optional): Password to unlock file from the hoster. Defaults to None.
                remote (str, optional): 0 or 1, use remote traffic. Defaults to None.

            Returns:
                requests.Response: Request object from requests library
            """
            return self.rd.post("/unrestrict/link", link=link, password=password, remote=remote)

        def folder(self, link: str) -> requests.Response:
            """Unrestrict a hoster folder link and get individual links

            Args:
                link (str): Original hoster link

            Returns:
                requests.Response: Request object from requests library (text returns an empty array if no links found)
            """
            return self.rd.post("/unrestrict/folder", link=link)

        def container_file(self, filepath: Path | str) -> requests.Response:
            """Decrypt a container file (RSDF, CCF, CCF3, DLC)

            Args:
                filepath (Path | str): Path to container file

            Returns:
                requests.Response: Request object from requests library
            """
            return self.rd.put("/unrestrict/containerFile", filepath=filepath)

        def container_link(self, link: str) -> requests.Response:
            """Decrypt a container file from a link

            Args:
                link (str): Link to the container file

            Returns:
                requests.Response: Request object from requests library
            """
            return self.rd.post("/unrestrict/containerLink", link=link)

    class Traffic:
        def __init__(self, rd: any) -> None:
            self.rd = rd

        def get(self) -> requests.Response:
            """Get traffic information for limited hosters

            Returns:
                requests.Response: Request object from requests library
            """
            return self.rd.get("/traffic")

        def details(self, start: str = None, end: str = None) -> requests.Response:
            """Get traffic details on each hoster during a defined period

            Args:
                start (str, optional): Start date (YYYY-MM-DD). Defaults to None (a week ago).
                end (str, optional): End date (YYYY-MM-DD). Defaults to None (today).

            Returns:
                requests.Response: Request object from requests library
            """
            return self.rd.get("/traffic/details", start=start, end=end)

    class Streaming:
        def __init__(self, rd: any) -> None:
            self.rd = rd

        def transcode(self, id: str) -> requests.Response:
            """Get transcoding links for given file

            Args:
                id (str): Torrent id from /downloads or /unrestrict/link

            Returns:
                requests.Response: Request object from requests library
            """
            return self.rd.get(f"/streaming/transcode/{id}")

        def media_infos(self, id: str) -> requests.Response:
            """Get detailled media informations for given file

            Args:
                id (str): Torrent id from /downloads or /unrestrict/link

            Returns:
                requests.Response: Request object from requests library
            """
            return self.rd.get(f"/streaming/mediaInfos/{id}")

    class Downloads:
        def __init__(self, rd: any) -> None:
            self.rd = rd

        def get(self, offset: int = None, page: int = None, limit: int = None) -> requests.Response:
            """Get user downloads list

            Args:
                offset (int, optional): Starting offset. Defaults to None.
                page (int, optional): Pagination system. Defaults to None.
                limit (int, optional): Entries returned per page / request (must be within 0 and 5000). Defaults to None (100).

            Returns:
                requests.Response: Request object from requests library
            """
            return self.rd.get("/downloads", offset=offset, page=page, limit=limit)

        def delete(self, id: str) -> requests.Response:
            """Delete a link from downloads list

            Args:
                id (str): Torrent id from /downloads or /unrestrict/link

            Returns:
                requests.Response: Request object from requests library
            """
            return self.rd.delete(f"/downloads/delete/{id}")

    class Torrents:
        def __init__(self, rd: any) -> None:
            self.rd = rd

        def get(
            self, offset: int = None, page: int = None, limit: int = None, filter: str = None
        ) -> requests.Response:
            """Get user torrents list

            Args:
                offset (int, optional): Starting offset. Defaults to None.
                page (int, optional): Pagination system. Defaults to None.
                limit (int, optional): Entries returned per page / request (must be within 0 and 5000). Defaults to None (100).
                filter (str, optional): "active", list active torrents only. Defaults to None.

            Returns:
                requests.Response: Request object from requests library
            """
            return self.rd.get("/torrents", offset=offset, page=page, limit=limit, filter=filter)

        def info(self, id: str) -> requests.Response:
            """Get information of a torrent

            Args:
                id (str): Torrent id from /downloads or /unrestrict/link

            Returns:
                requests.Response: Request object from requests library
            """
            return self.rd.get(f"/torrents/info/{id}")

        def instant_availability(self, hash: str) -> requests.Response:
            """Get list of instantly available file IDs by hoster

            Args:
                hash (str): SHA1 of the torrent

            Returns:
                requests.Response: Request object from requests library
            """
            return self.rd.get(f"/torrents/instantAvailability/{hash}")

        def active_count(self) -> requests.Response:
            """Get currently active torrents number and the current maximum limit

            Returns:
                requests.Response: Request object from requests library
            """
            return self.rd.get("/torrents/activeCount")

        def available_hosts(self) -> requests.Response:
            """Get available hosts to upload the torrent to

            Returns:
                requests.Response: Request object from requests library
            """
            return self.rd.get("/torrents/availableHosts")

        def add_torrent(self, filepath: Path | str, host: str = None) -> requests.Response:
            """Add a torrent file to download

            Args:
                filepath (Path | str): Path to torrent file
                host (str, optional): Hoster domain (from torrents.available_hosts). Defaults to None.

            Returns:
                requests.Response: Request object from requests library
            """
            return self.rd.put("/torrents/addTorrent", filepath=filepath, host=host)

        def add_magnet(self, magnet: str, host: str = None) -> requests.Response:
            """Add a magnet link to download

            Args:
                magnet (str): Manget link
                host (str, optional): Hoster domain (from torrents.available_hosts). Defaults to None.

            Returns:
                requests.Response: Request object from requests library
            """
            return self.rd.post("/torrents/addMagnet", magnet=f"magnet:?xt=urn:btih:{magnet}", host=host)

        def select_files(self, id: str, files: str) -> requests.Response:
            """Select files of a torrent to start it

            Args:
                id (str): Torrent id from /downloads or /unrestrict/link
                files (str): Selected files IDs (comma separated) or "all"

            Returns:
                requests.Response: Request object from requests library
            """
            return self.rd.post(f"/torrents/selectFiles/{id}", files=files)

        def delete(self, id: str) -> requests.Response:
            """Delete a torrent from torrents list

            Args:
                id (str): Torrent id from /downloads or /unrestrict/link

            Returns:
                requests.Response: Request object from requests library
            """
            return self.rd.delete(f"/torrents/delete/{id}")

    class Hosts:
        def __init__(self, rd: any) -> None:
            self.rd = rd

        def get(self) -> requests.Response:
            """Get supported hosts

            Returns:
                requests.Response: Request object from requests library
            """
            return self.rd.get("/hosts")

        def status(self) -> requests.Response:
            """Get status of supported hosters, and from competetors

            Returns:
                requests.Response: Request object from requests library
            """
            return self.rd.get("/hosts/status")

        def regex(self) -> requests.Response:
            """Get all supported links regex

            Returns:
                requests.Response: Request object from requests library
            """
            return self.rd.get("/hosts/regex")

        def regex_folder(self) -> requests.Response:
            """Get all supported folder regex

            Returns:
                requests.Response: Request object from requests library
            """
            return self.rd.get("/hosts/regexFolder")

        def domains(self) -> requests.Response:
            """Get all supported hoster domains

            Returns:
                requests.Response: Request object from requests library
            """
            return self.rd.get("/hosts/domains")

    class Settings:
        def __init__(self, rd: any) -> None:
            self.rd = rd

        def get(self) -> requests.Response:
            """Get current user settings with possible values to update

            Returns:
                requests.Response: Request object from requests library
            """
            return self.rd.get("/settings")

        def update(self, setting_name: str, setting_value: str) -> requests.Response:
            """Update a user setting

            Args:
                setting_name (str): Setting name
                setting_value (str): Setting value

            Returns:
                requests.Response: Request object from requests library
            """
            return self.rd.post("/settings/update", setting_name=setting_name, setting_value=setting_value)

        def convert_points(self) -> requests.Response:
            """Convert fidelity points

            Returns:
                requests.Response: Request object from requests library
            """
            return self.rd.post("/settings/convertPoints")

        def change_password(self) -> requests.Response:
            """Send the verification email to change the account password

            Returns:
                requests.Response: Request object from requests library
            """
            return self.rd.post("/settings/changePassword")

        def avatar_file(self, filepath: Path | str) -> requests.Response:
            """Upload a new user avatar image

            Args:
                filepath (Path | str): Path to the avatar url

            Returns:
                requests.Response: Request object from requests library
            """
            return self.rd.put("/settings/avatarFile", filepath=filepath)

        def avatar_delete(self) -> requests.Response:
            """Reset user avatar image to default

            Returns:
                requests.Response: Request object from requests library
            """
            return self.rd.delete("/settings/avatarDelete")
