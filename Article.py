# ---------------------------------------------------------------------------------
# Name: Article
# Description: Displays your article Criminal Code of the Russian Federation
# Author: @hikka_mods
# ---------------------------------------------------------------------------------

# 🔒    Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# ⚠️ Where is the JoinChannelRequest

# meta developer: @hikka_mods
# scope: Article
# scope: Article 0.0.1
# requires: requests
# ---------------------------------------------------------------------------------

import json
import random
import requests
import logging
from typing import Dict
from hikkatl.types import Message
from telethon.tl.functions.channels import JoinChannelRequest

from .. import loader, utils

logger = logging.getLogger(__name__)


@loader.tds
class ArticleMod(loader.Module):
    """Displays your article Criminal Code of the Russian Federation"""

    strings = {
        "name": "Article",
        "article": "<emoji document_id=5226512880362332956>📖</emoji> <b>Твоя статья УК РФ</b>:\n\n<blockquote>Номер {}\n\n{}</blockquote>",
    }

    async def arccmd(self, message: Message):
        """Displays your article Criminal Code of the Russian Federation"""
        values = self._load_values()
        if values:
            random_key = random.choice(list(values.keys()))
            random_value = values[random_key]
            await utils.answer(
                message, self.strings("article").format(random_key, random_value)
            )

    def _load_values(self) -> Dict[str, str]:
        url = "https://raw.githubusercontent.com/Codwizer/ReModules/main/assets/zakon.json"
        try:
            response = requests.get(url)
            if response.ok:
                data = json.loads(response.text)
                return data
        except (requests.RequestException, json.JSONDecodeError):
            pass

        return {}
