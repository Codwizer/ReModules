# ---------------------------------------------------------------------------------
# Name: animals
# Description: Random cats and dogs
# Author: @hikka_mods
# ---------------------------------------------------------------------------------

# 🔒    Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# meta developer: @hikka_mods
# scope: Api animals
# scope: Api animals 0.0.1
# requires: requests
# ---------------------------------------------------------------------------------
from hikkatl.types import Message
import requests

from .. import loader, utils

__version__ = (1, 0, 0)


@loader.tds
class animals(loader.Module):
    """Random cats and dogs"""

    strings = {
        "name": "animals",
        "loading": "<b>Generation is underway</b>",
        "done": "<b>Here is your salute</b>",
    }

    strings_ru = {
        "loading": "<b>Генерация идет полным ходом</b>",
        "done": "<b>Вот ваш результат</b>",
    }

    async def fcatcmd(self, message: Message):
        """random photos of cats files"""
        await utils.answer(message, self.strings("loading"))
        response = requests.get("https://api.thecatapi.com/v1/images/search")
        cat_url = response.json()[0]["url"]
        await utils.answer_file(
            message, cat_url, self.strings("done"), force_document=True
        )

    async def fdogcmd(self, message: Message):
        """random photos of dog files"""
        await utils.answer(message, self.strings("loading"))
        response = requests.get("https://api.thedogapi.com/v1/images/search")
        dog_url = response.json()[0]["url"]
        await utils.answer_file(
            message, dog_url, self.strings("done"), force_document=True
        )

    async def catcmd(self, message: Message):
        """random photos of cats"""
        await utils.answer(message, self.strings("loading"))
        response = requests.get("https://api.thecatapi.com/v1/images/search")
        cat_url = response.json()[0]["url"]
        await utils.answer_file(
            message, cat_url, self.strings("done"), force_document=False
        )

    async def dogcmd(self, message: Message):
        """random photos of dog"""
        await utils.answer(message, self.strings("loading"))
        response = requests.get("https://api.thedogapi.com/v1/images/search")
        dog_url = response.json()[0]["url"]
        await utils.answer_file(
            message, dog_url, self.strings("done"), force_document=False
        )
