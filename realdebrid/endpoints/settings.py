import aiohttp

from pathlib import Path


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
