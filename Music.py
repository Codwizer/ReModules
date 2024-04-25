# ---------------------------------------------------------------------------------
# Name: Music
# Description: Search for music through music bots.
# Author: @hikka_mods
# Commands:
# ym / vkm
# ---------------------------------------------------------------------------------

# 🔒    Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# meta developer: @hikka_mods
# scope: Music
# scope: Music 0.0.1
# ---------------------------------------------------------------------------------
from .. import loader, utils

__version__ = (1, 0, 0)


@loader.tds
class MusicMod(loader.Module):
    """Поиск музыки через музыкальных ботов."""

    strings = {
        "name": "Music",
        "nenashel": (
            "<emoji document_id=5337117114392127164>🤷‍♂</emoji> <b>And what should I look for?</b>"
        ),
        "searching": "<emoji document_id=4918235297679934237>⌨️</emoji> <b>Searching...</b>",
        "done": "<emoji document_id=5336965905773504919>🗣</emoji> <b>Perhaps this is the track you were looking for</b>",
        "error": "<emoji document_id=5228947933545635555>😫</emoji> <b>I couldn't find a track with the title <code>{}</code></b>",
    }

    strings_ru = {
        "nenashel": (
            "<emoji document_id=5337117114392127164>🤷‍♂</emoji> <b>А что искать то?</b>"
        ),
        "searching": "<emoji document_id=4918235297679934237>⌨️</emoji> <b>Поиск...</b>",
        "done": "<emoji document_id=5336965905773504919>🗣</emoji> <b>Возможно, это тот трек, который вы искали</b>",
        "error": "<emoji document_id=5228947933545635555>😫</emoji> <b>Я не смог найти трек с названием <code>{}</code><b>",
    }

    async def ymcmd(self, message):
        """- найти трек по названию из Yandex music"""
        args = utils.get_args_raw(message)
        r = await message.get_reply_message()
        bot = "@Yandex_music_download_bot"
        if not args:
            return await message.edit(self.strings("nenashel"))
        try:
            await message.edit(self.strings("searching"))
            music = await message.client.inline_query(bot, args)
            await message.delete()
            try:
                await message.client.send_file(
                    message.to_id,
                    music[1].result.document,
                    caption=self.strings("done"),
                    reply_to=utils.get_topic(message) if r else None,
                )
            except:
                await message.client.send_file(
                    message.to_id,
                    music[3].result.document,
                    caption=self.strings("done"),
                    reply_to=utils.get_topic(message) if r else None,
                )
        except:
            return await message.client.send_message(
                message.chat_id, self.strings("error").format(args=args)
            )

    async def vkmcmd(self, message):
        """- найти трек по названию из VK"""
        args = utils.get_args_raw(message)
        r = await message.get_reply_message()
        bot = "@vkmusic_bot"
        if not args:
            return await message.edit(self.strings("nenashel"))
        try:
            await message.edit(self.strings("searching"))
            music = await message.client.inline_query(bot, args)
            await message.delete()
            try:
                await message.client.send_file(
                    message.to_id,
                    music[1].result.document,
                    caption=self.strings("done"),
                    reply_to=utils.get_topic(message) if r else None,
                )
            except:
                await message.client.send_file(
                    message.to_id,
                    music[3].result.document,
                    caption=self.strings("done"),
                    reply_to=utils.get_topic(message) if r else None,
                )
        except:
            return await message.client.send_message(
                message.chat_id, self.strings("error").format(args=args)
            )
