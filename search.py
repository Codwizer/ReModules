# ---------------------------------------------------------------------------------
# Name: Search
# Description: Search for your question on the Internet
# Author: @hikka_mods
# ---------------------------------------------------------------------------------

# 🔒    Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# meta developer: @hikka_mods
# scope: Api Search
# scope: Api Search 0.0.1
# ---------------------------------------------------------------------------------

from telethon.tl.types import Message  # type: ignore
from urllib.parse import quote

from .. import loader, utils
from ..inline.types import InlineCall, InlineQuery

__version__ = (1, 0, 0)


@loader.tds
class Search(loader.Module):
    """Поисковик"""

    strings = {
        "name": "Search",
        "search": "<emoji document_id=5188311512791393083>🌎</emoji><b> I searched for information for you</b> ",
        "isearch": "🔎<b> I searched for information for you</b> ",
        "link": "🗂️ Link to your request",
        "close": "❌ Close",
    }

    strings_ru = {
        "search": "<emoji document_id=5188311512791393083>🌎</emoji><b> Я поискал информацию за тебя</b> ",
        "isearch": "🔎<b> Я поискал информацию за тебя</b> ",
        "link": "🗂️ Ссылка на ваш запрос",
        "close": "❌ Закрыть",
    }

    async def googlecmd(self, message: Message):
        """поискать в Google"""
        g = utils.get_args_raw(message)
        google = f"https://google.com/search?q={g}"
        await utils.answer(
            message, self.strings("search") + f'<a href="{google}">Ссылка</a>'
        )

    async def yandexcmd(self, message: Message):
        """поискать в Yandex"""
        y = utils.get_args_raw(message)
        yandex = f"https://yandex.ru/?q={y}"
        await utils.answer(
            message, self.strings("search") + f'<a href="{yandex}">Ссылка</a>'
        )

    async def duckduckgocmd(self, message: Message):
        """поискать в Duckduckgo"""
        d = utils.get_args_raw(message)
        duckduckgo = f"https://duckduckgo.com/?q={d}"
        await utils.answer(
            message, self.strings("search") + f'<a href="{duckduckgo}">Ссылка</a>'
        )

    async def bingcmd(self, message: Message):
        """поискать в Bing"""
        b = utils.get_args_raw(message)
        bing = f"https://bing.com/?q={b}"
        await utils.answer(
            message, self.strings("search") + f'<a href="{bing}">Ссылка</a>'
        )

    async def youcmd(self, message: Message):
        """поискать в You"""
        y = utils.get_args_raw(message)
        you = f"https://you.com/?q={y}"
        await utils.answer(
            message, self.strings("search") + f'<a href="{you}">Ссылка</a>'
        )

    async def igooglecmd(self, message: Message):
        """поискать в Google инлайн"""
        g = utils.get_args_raw(message)
        google = f"https://google.com/search?q={g}"
        await self.inline.form(
            text=self.strings("isearch"),
            message=message,
            reply_markup=[
                [
                    {
                        "text": self.strings("link"),
                        "url": google,
                    }
                ],
                [{"text": self.strings("close"), "action": "close"}],
            ],
            silent=True,
        )

    async def iyandexcmd(self, message: Message):
        """поискать в Yandex инлайн"""
        y = utils.get_args_raw(message)
        yandex = f"https://yandex.ru/?q={y}"
        await self.inline.form(
            text=self.strings("isearch"),
            message=message,
            reply_markup=[
                [
                    {
                        "text": self.strings("link"),
                        "url": yandex,
                    }
                ],
                [{"text": self.strings("close"), "action": "close"}],
            ],
            silent=True,
        )

    async def iduckduckgocmd(self, message: Message):
        """поискать в Duckduckgo инлайн"""
        d = utils.get_args_raw(message)
        duckduckgo = f"https://duckduckgo.com/?q={d}"
        await self.inline.form(
            text=self.strings("isearch"),
            message=message,
            reply_markup=[
                [
                    {
                        "text": self.strings("link"),
                        "url": duckduckgo,
                    }
                ],
                [{"text": self.strings("close"), "action": "close"}],
            ],
            silent=True,
        )

    async def ibingcmd(self, message: Message):
        """поискать в Bing инлайн"""
        b = utils.get_args_raw(message)
        bing = f"https://bing.com/?q={b}"
        await self.inline.form(
            text=self.strings("isearch"),
            message=message,
            reply_markup=[
                [
                    {
                        "text": self.strings("link"),
                        "url": bing,
                    }
                ],
                [{"text": self.strings("close"), "action": "close"}],
            ],
            silent=True,
        )

    async def iyoucmd(self, message: Message):
        """поискать в You инлайн"""
        y = utils.get_args_raw(message)
        you = f"https://you.com/?q={y}"
        await self.inline.form(
            text=self.strings("isearch"),
            message=message,
            reply_markup=[
                [
                    {
                        "text": self.strings("link"),
                        "url": you,
                    }
                ],
                [{"text": self.strings("close"), "action": "close"}],
            ],
            silent=True,
        )

    async def close(self, call):
        """Callback button"""
        await call.delete()
