# ---------------------------------------------------------------------------------
# Name: InlineCoin
# Description: Mini game heads or tails.
# Author: @hikka_mods
# ---------------------------------------------------------------------------------

# 🔒    Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# meta developer: @hikka_mods
# scope: InlineCoin
# scope: InlineCoin 0.0.1
# ---------------------------------------------------------------------------------
from .. import loader, utils
from telethon.tl.types import Message
import random

from ..inline.types import InlineQuery

coin = [
    "🌚 Выпал орёл!",
    "🌝 Выпала решка!",
    "🙀 Чудо, монетка осталась на ребре!",
    "🌚 Выпал орёл!",
    "🌚 Выпал орёл!",
    "🌝 Выпала решка!",
    "🌝 Выпала решка!",
]


@loader.tds
class CoinSexMod(loader.Module):
    """Mini game heads or tails"""

    strings = {"name": "InlineCoin"}

    @loader.inline_everyone
    async def coin_inline_handler(self, query: InlineQuery):
        coinrand = random.choice(coin)
        return {
            "title": "Орёл или решка?",
            "description": "Давай узнаем!",
            "message": f"<b>{coinrand}</b>",
            "thumb": "https://codwiz.site/files/coin.png",
        }
