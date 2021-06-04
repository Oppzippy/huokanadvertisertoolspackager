import unittest
import zipfile
import os
from huokanadvertisertools import HuokanAdvertiserToolsPackager


class TestHuokanAdvertiserTools(unittest.TestCase):
    def test_set_name(self):
        hat = HuokanAdvertiserToolsPackager(
            os.path.join(
                os.path.dirname(os.path.realpath(__file__)), "HuokanAdvertiserTools.zip"
            )
        )
        hat.set_discord_tag("name-realm")
        with hat.create_customized_addon_zip() as hat_bytes:
            with zipfile.ZipFile(hat_bytes, "r") as zip:
                content = zip.read("HuokanAdvertiserTools/Custom.lua").decode("utf-8")
                self.assertIn('addon.discordTag = "name-realm"', content)
            with open("hat.zip", "wb") as f:
                f.write(hat_bytes.getvalue())