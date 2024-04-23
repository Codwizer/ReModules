# Name: Kittens
# Description: Module for search cutie kitties from @catslovemeow
# Author: @nervousmods
# Commands:
# .kit
# ---------------------------------------------------------------------------------
# 🔒 Licensed under the GNU GPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html
# ⚠️ All modules is not scam and absolutely safe.
# 👤 https://t.me/smlgwy
#-----------------------------------------------------------------------------------
# meta developer: @nervousmods, @hikka_mods
#scope: hikka_only 
#scope: hikka_min 1.4.2
#-----------------------------------------------------------------------------------

from .. import loader
import logging
from telethon.tl.custom import Message
import datetime
from telethon import functions
import random
import time

__version__ = (1, 0, 0)
logger = logging.getLogger(__name__)


@loader.tds
class Kittens(loader.Module):
    """Module for search cutie kitties from @catslovemeow"""
    strings = {
        "name": "Kittens"
    }

    @loader.command()
    async def kitcmd(self, message: Message):
        """-> to get a cute kitty"""
        await message.edit("<emoji document_id=5328311576736833844>🔴</emoji>Search cutie kitties..")
        time.sleep(1)
        chat = "catslovemeow"
        result = await message.client(functions.messages.GetHistoryRequest(
            peer=chat,
            offset_id = 0,
offset_date = datetime.datetime.now(),
add_offset = random.choice(range(1, 101, 2)),
        limit = 1,
        max_id = 0,
        min_id = 0,
        hash = 0,
        ),
    )
        await message.delete()
        await message.client.send_file(message.to_id, result.messages[0].media)
