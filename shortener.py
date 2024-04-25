# ---------------------------------------------------------------------------------
# Name: Shortener
# Description: shortening the link
# Author: @hikka_mods
# ---------------------------------------------------------------------------------

# 🔒    Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# meta developer: @hikka_mods
# scope: Shortener
# scope: Shortener 0.0.1
# requires: pyshorteners
# ---------------------------------------------------------------------------------
from hikkatl.types import Message
from .. import loader, utils
import pyshorteners

__version__ = (1, 0, 0)


@loader.tds
class Shortener(loader.Module):
    """Module for working with the api bit.ly"""

    strings = {
        "name": "Shortener",
        "no_api": "<emoji document_id=5854929766146118183>❌</emoji> You have not specified an API token from the site <a href='https://app.bitly.com/settings/api/'>bit.ly</a>",
        "statclcmd": "<emoji document_id=5787384838411522455>📊</emoji> <b>Statistics on clicks for this link:</b> {c}",
        "shortencmd": "<emoji document_id=5854762571659218443>✅</emoji> <b>Your shortened link is ready:</b> <code>{c}</code>",
    }

    strings_ru = {
        "no_api": "<emoji document_id=5854929766146118183>❌</emoji> Вы не указали api токен с сайта <a href='https://app.bitly.com/settings/api/'>bit.ly</a>",
        "statclcmd": "<emoji document_id=5787384838411522455>📊</emoji> <b>Статистика о переходе по этой ссылке:</b> {c}",
        "shortencmd": "<emoji document_id=5854762571659218443>✅</emoji> <b>Ваша сокращённая ссылка готова:</b> <code>{c}</code>",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "token",
                None,
                lambda: "Need a token with https://app.bitly.com/settings/api/",
                validator=loader.validators.Hidden(),
            )
        )

    async def shortencmd(self, message: Message):
        """сократить ссылку через bit.ly"""
        if self.config["token"] is None:
            await utils.answer(message, self.strings("no_api"))
            return

        s = pyshorteners.Shortener(api_key=self.config["token"])
        args = utils.get_args_raw(message)
        await utils.answer(
            message, self.strings("shortencmd").format(c=s.bitly.short(args))
        )

    async def statclcmd(self, message: Message):
        """посмотреть статистику ссылки через bit.ly"""
        if self.config["token"] is None:
            await utils.answer(message, self.strings("no_api"))
            return

        s = pyshorteners.Shortener(api_key=self.config["token"])
        args = utils.get_args_raw(message)
        await utils.answer(
            message, self.strings("statclcmd").format(c=s.bitly.total_clicks(args))
        )
