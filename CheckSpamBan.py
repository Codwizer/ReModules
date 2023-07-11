# ---------------------------------------------------------------------------------
# Name: CheckSpamBan
# Description: Check spam ban for your account.
# Author: @hikka_mods
# ---------------------------------------------------------------------------------

# 🔒    Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# meta developer: @hikka_mods
# scope: CheckSpamBan
# scope: CheckSpamBan 0.0.1
# ---------------------------------------------------------------------------------

from .. import loader, utils
from ..utils import answer
from telethon.tl.types import Message

@loader.tds
class SpamBanCheckMod(loader.Module):
    """Check spam ban for your account."""
    strings = {
        "name": "CheckSpamBan",
    }

    @loader.command()
    async def spamban(self, message: Message):
        """- checks your account for spam ban via @SpamBot bot."""
        async with self._client.conversation("@SpamBot") as conv:
            msg = await conv.send_message("/start")
            r = await conv.get_response()
            if r.text == 'Ваш аккаунт свободен от каких-либо ограничений.':
                text = "<b>Все прекрасно!\nУ вас нет спам бана.</b>"
            else:
                kk = r.text.split('\n')[2]
                ll = r.text.split('\n')[4]
                text = f"<b>К сожалению ваш аккаунт получил спам-бан...\n\n{kk}\n\n{ll}</b>"
            await msg.delete()
        await r.delete()
        await answer(message, text)
