import zipfile
import io
from typing import Union
from pathlib import Path


class HuokanAdvertiserToolsPackager:
    def __init__(self, addon_zip_path: Union[Path, str] = "HuokanAdvertiserTools.zip"):
        """Creates a copy of Huokan Advertiser Tools which can be customized to have options for specific users.

        Args:
            addon_zip_path (str, optional): Path to the unmodified addon zip file. Defaults to 'HuokanAdvertiserTools.zip'.
        """
        self.addon_zip_path = addon_zip_path
        self.custom_script_lines = ["local _, addon = ...", ""]

    def set_discord_tag(self, discord_tag: str) -> None:
        """Configures the addon's discord tag option. This may not be changed by the user without modifying the addon.

        Args:
            discord_tag (str): Discord tag of the user for whom the addon is being configured.
        """
        discord_tag_escaped = discord_tag.replace('"', '\\"')
        self.custom_script_lines.append(f'addon.discordTag = "{discord_tag_escaped}"')

    def get_custom_script(self) -> str:
        """Returns the generated content of Custom.lua.

        Returns:
            str: Custom script for Custom.lua
        """
        custom_script = "\n".join(self.custom_script_lines)
        return f"{custom_script}\n"

    def create_customized_addon_zip(self) -> io.BytesIO:
        """Creates a copy of the addon zip file with the Custom.lua script file modified.

        Returns:
            io.BytesIO: Customized addon zip file.
        """
        custom_copy_bytes = self._create_copy_without_files(
            ["HuokanAdvertiserTools/Custom.lua"]
        )

        with zipfile.ZipFile(
            custom_copy_bytes, "a", zipfile.ZIP_DEFLATED, compresslevel=9
        ) as custom_copy_zip:
            custom_copy_zip.writestr(
                "HuokanAdvertiserTools/Custom.lua", self.get_custom_script()
            )
        custom_copy_bytes.seek(0)

        return custom_copy_bytes

    def _create_copy_without_files(self, blacklist: list) -> io.BytesIO:
        """Creates a copy of the addon zip file with the provided files excluded.

        Args:
            blacklist (list): File paths within the zip to exclude from the copy.

        Returns:
            io.BytesIO: Addon zip excluding the blacklisted files.
        """
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(self.addon_zip_path, "r") as zip_in:
            with zipfile.ZipFile(
                zip_buffer, "w", zipfile.ZIP_DEFLATED, compresslevel=9
            ) as zip_out:
                for item in zip_in.infolist():
                    if item.filename not in blacklist:
                        zip_out.writestr(item, zip_in.read(item.filename))
        zip_buffer.seek(0)
        return zip_buffer
