# ---------------------------------------------------------------------------------
# Name: AutofarmCookies
# Description: Autofarm in the bot @cookies_game_bot
# Author: @hikka_mods
# ---------------------------------------------------------------------------------

# 🔒    Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# meta developer: @hikka_mods
# scope: AutofarmCookies
# scope: AutofarmCookies 0.0.1
# ---------------------------------------------------------------------------------

import random
from datetime import timedelta

from telethon import functions
from telethon.tl.types import Message

from .. import loader, utils

__version__ = (1, 0, 0)


@loader.tds
class AutofarmCookiesMod(loader.Module):
    """Autofarm in the bot @cookies_game_bot"""

    strings = {
        "name": "AutofarmCookies",
        "farmon": (
            "<i>The deferred task has been created, autofarming has been started, everything will start in 10 minutes"
            " seconds...</i>"
        ),
        "farmon_already": "<i>It has already been launched :)</i>",
        "farmoff": "<i>The autopharm is stopped\nSelected:</i> <b>%coins% Cookies</b>",
        "farm": "<i>I typed:</i> <b>%coins% Cookies</b>",
    }

    strings_ru = {
        "farmon": (
            "<i>Отложенная задача создана, автофарминг запущен, всё начнётся через 10"
            " секунд...</i>"
        ),
        "farmon_already": "<i>Уже запущено :)</i>",
        "farmoff": "<i>Автофарм остановлен.\nНвброно:</i> <b>%coins% Cookies</b>",
        "farm": "<i>Я набрал:</i> <b>%coins% Cookies</b>",
    }

    def __init__(self):
        self.name = self.strings["name"]

    async def client_ready(self, client, db):
        self.client = client
        self.db = db
        self.myid = (await client.get_me()).id
        self.cookies = 5203407003

    @loader.command()
    async def cookoncmd(self, message):
        """Запустить автофарминг"""
        status = self.db.get(self.name, "status", False)
        if status:
            return await message.edit(self.strings["farmon_already"])
        self.db.set(self.name, "status", True)
        await self.client.send_message(
            self.cookies, "/cookie", schedule=timedelta(seconds=10)
        )
        await message.edit(self.strings["farmon"])

    @loader.command()
    async def cookoffcmd(self, message):
        """Остановить автофарминг"""
        self.db.set(self.name, "status", False)
        coins = self.db.get(self.name, "coins", 0)
        if coins:
            self.db.set(self.name, "coins", 0)
        await message.edit(self.strings["farmoff"].replace("%coins%", str(coins)))

    @loader.command()
    async def cookiescmd(self, message):
        """Вывод кол-ва коинов, добытых этим модулем"""
        coins = self.db.get(self.name, "coins", 0)
        await message.edit(self.strings["farm"].replace("%coins%", str(coins)))

    async def watcher(self, event):
        if not isinstance(event, Message):
            return
        chat = utils.get_chat_id(event)
        if chat != self.cookies:
            return
        status = self.db.get(self.name, "status", False)
        if not status:
            return
        if event.raw_text == "/cookie":
            return await self.client.send_message(
                self.cookies, "/cookie", schedule=timedelta(hours=2)
            )
        if event.sender_id != self.cookies:
            return
        if "🙅‍♂️!" in event.raw_text:
            args = [int(x) for x in event.raw_text.split() if x.isnumeric()]
            randelta = random.randint(20, 60)
            if len(args) == 4:
                delta = timedelta(
                    hours=args[1], minutes=args[2], seconds=args[3] + randelta
                )
            elif len(args) == 3:
                delta = timedelta(minutes=args[1], seconds=args[2] + randelta)
            elif len(args) == 2:
                delta = timedelta(seconds=args[1] + randelta)
            else:
                return
            sch = (
                await self.client(
                    functions.messages.GetScheduledHistoryRequest(self.cookies, 1488)
                )
            ).messages
            await self.client(
                functions.messages.DeleteScheduledMessagesRequest(
                    self.cookies, id=[x.id for x in sch]
                )
            )
            return await self.client.send_message(
                self.cookies, "/cookie", schedule=delta
            )
        if "✨" in event.raw_text:
            args = event.raw_text.split()
            for x in args:
                if x[0] == "+":
                    return self.db.set(
                        self.name,
                        "coins",
                        self.db.get(self.name, "coins", 0) + int(x[1:]),
                    )

    async def message_q(
        self,
        text: str,
        user_id: int,
        mark_read: bool = False,
        delete: bool = False,
    ):
        """Отправляет сообщение и возращает ответ"""
        async with self.client.conversation(user_id) as conv:
            msg = await conv.send_message(text)
            response = await conv.get_response()
            if mark_read:
                await conv.mark_read()

            if delete:
                await msg.delete()
                await response.delete()

            return response

    @loader.command()
    async def mecmd(self, message):
        """Показывает ваш мешок"""

        bot = "@cookies_game_bot"
        bags = await self.message_q(
            "/me",
            bot,
            delete=True,
        )

        args = utils.get_args_raw(message)

        if not args:
            await utils.answer(message, bags.text)

    @loader.command()
    async def ckiescmd(self, message):
        """Помощь по модулю AutofarmCookies"""
        chelp = """
🍀| <b>Помощь по командам:</b>
.cookon - Включает авто фарм.
.cookoff - Выключает авто фарм.
.farm - Показывает сколько вы нафармили.
.me - Показывает ваш ммешок"""
        await utils.answer(message, chelp)
