import unittest
import zipfile
import os
from huokanadvertisertoolspackager import HuokanAdvertiserToolsPackager


class TestHuokanAdvertiserTools(unittest.TestCase):
    def test_set_name(self):
        hat = HuokanAdvertiserToolsPackager(
            os.path.join(
                os.path.dirname(os.path.realpath(__file__)), "HuokanAdvertiserTools.zip"
            )
        )
        hat.set_discord_tag("name-realm")
        with hat.create_addon_zip() as zip_bytes:
            with zipfile.ZipFile(zip_bytes, "r") as zip:
                content = zip.read("HuokanAdvertiserTools/Custom.lua").decode("utf-8")
                self.assertIn('addon.discordTag = "name-realm"', content)
