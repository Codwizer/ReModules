# ---------------------------------------------------------------------------------
# Name: face
# Description: Random face
# Author: @hikka_mods
# ---------------------------------------------------------------------------------

# 🔒    Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# meta developer: @hikka_mods
# scope: Api face
# scope: Api face 0.0.1
# requires: requests
# ---------------------------------------------------------------------------------
from hikkatl.types import Message
import requests

from .. import loader, utils

__version__ = (1, 0, 0)


@loader.tds
class face(loader.Module):
    """random face"""

    strings = {
        "name": "face",
        "loading": (
            "<emoji document_id=5348399448017871250>🔍</emoji> I'm looking for you kaomoji"
        ),
        "random_face": (
            "<emoji document_id=5208878706717636743>🗿</emoji> Here is your random one kaomoji\n<code>{}</code>"
        ),
    }

    strings_ru = {
        "loading": (
            "<emoji document_id=5348399448017871250>🔍</emoji> Ищю вам kaomoji"
        ),
        "random_face": (
            "<emoji document_id=5208878706717636743>🗿</emoji> Вот ваш рандомный kaomoji\n<code>{}</code>"
        ),
    }

    async def rfacecmd(self, message: Message):
        """random kaomoji"""
        await utils.answer(message, self.strings("loading"))
        response = requests.get("https://vsecoder.dev/api/faces")
        random_face = response.json()["data"]
        await utils.answer(message, self.strings("random_face").format(random_face))
