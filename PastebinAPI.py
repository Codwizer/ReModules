# ---------------------------------------------------------------------------------
# Name: PastebinAPI
# Description: fills in the code on pastebin
# Author: @hikka_mods
# ---------------------------------------------------------------------------------

# 🔒    Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# meta developer: @hikka_mods
# scope: PastebinAPI
# scope: PastebinAPI 0.0.1
# requires: aiohttp
# ---------------------------------------------------------------------------------

import asyncio
import json
import aiohttp
from requests import get
from hikkatl.tl.types import Message

from .. import loader, utils

@loader.tds
class PastebinAPIMod(loader.Module):
    """PastebinAPI"""

    strings = {
        "name": "PastebinAPI",
        "no_reply": "<emoji document_id=5462882007451185227>🚫</emoji> Вы не указали текст",
        "no_key": "<emoji document_id=5843952899184398024>🚫</emoji> Ключ не найден",
        "done": "Ваша ссылка с кодом\n<emoji document_id=5985571061993837069>➡️</emoji> <code>{response_text}</code>"
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
            "pastebin",
            None,
            lambda: "link to get api https://pastebin.com/doc_api#1",
            validator=loader.validators.Hidden()
            )
         )

    async def pastcmd(self, message):
        """Заливает код в Pastebin"""
        text = utils.get_args(message)

        if self.config["pastebin"] is None:
            await utils.answer(message, self.strings("no_key"))
            return

        if not text:
            await utils.answer(message, self.strings("no_reply"))
            return

        async with aiohttp.ClientSession() as Session:
            async with Session.post(
                url='https://pastebin.com/api/api_post.php',
                data={
                    'api_dev_key': self.config["pastebin"] ,
                    'api_paste_code': text,
                    'api_option': 'paste'
                }) as response:

                response_text = await response.text()

                await utils.answer(message, self.strings("done").format(response_text=response_text))
