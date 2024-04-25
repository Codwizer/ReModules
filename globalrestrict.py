#             █ █ ▀ █▄▀ ▄▀█ █▀█ ▀
#             █▀█ █ █ █ █▀█ █▀▄ █
#              © Copyright 2022
#           https://t.me/hikariatama
#
# 🔒      Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# Some functions took from Hikarichat by Hikariatama

# ---------------------------------------------------------------------------------
# Name: GlobalRestrict
# Description: Global mutation or ban
# Author: @hikka_mods
# ---------------------------------------------------------------------------------

# 🔒    Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# meta developer: @hikka_mods
# scope: Api GlobalRestrict
# scope: Api GlobalRestrict 0.0.1
# ---------------------------------------------------------------------------------

import re
import time
import typing

from telethon.tl.functions.channels import (
    JoinChannelRequest,
    EditAdminRequest,
    EditBannedRequest,
    GetFullChannelRequest,
    GetParticipantRequest,
    InviteToChannelRequest,
)
from telethon.tl.functions.messages import EditChatDefaultBannedRightsRequest
from telethon.tl.types import (
    Channel,
    ChannelParticipantCreator,
    Chat,
    ChatAdminRights,
    ChatBannedRights,
    DocumentAttributeAnimated,
    Message,
    MessageEntitySpoiler,
    MessageMediaUnsupported,
    User,
    UserStatusOnline,
)

from telethon.tl.types import (
    Channel,
    Chat,
    Message,
    User,
)

from .. import loader, utils

__version__ = (1, 0, 0)

BANNED_RIGHTS = {
    "view_messages": False,
    "send_messages": False,
    "send_media": False,
    "send_stickers": False,
    "send_gifs": False,
    "send_games": False,
    "send_inline": False,
    "send_polls": False,
    "change_info": False,
    "invite_users": False,
}

MUTES_RIGHTS = {
    "view_messages": True,
    "send_messages": False,
    "send_media": False,
    "send_stickers": False,
    "send_gifs": False,
    "send_games": False,
    "send_inline": False,
    "send_polls": False,
    "change_info": False,
    "invite_users": False,
}


def get_full_name(user: typing.Union[User, Channel]) -> str:
    return utils.escape_html(
        user.title
        if isinstance(user, Channel)
        else (
            f"{user.first_name} "
            + (user.last_name if getattr(user, "last_name", False) else "")
        )
    ).strip()


@loader.tds
class GlobalRestrict(loader.Module):
    """Global mutation or ban"""

    strings = {
        "name": "GlobalRestrict",
        "no_reason": "Not specified",
        "args": (
            "<emoji document_id=5300759756669984376>🚫</emoji> <b>Incorrect arguments</b>"
        ),
        "glban": (
            '<emoji document_id=5301059317753979286>🖕</emoji> <b><a href="{}">{}</a>'
            " has been globally banned.</b>\n<b>Reason: </b><i>{}</i>\n\n{}"
        ),
        "glbanning": (
            "<emoji document_id=5301059317753979286>🖕</emoji> <b>Globally banning <a"
            ' href="{}">{}</a>...</b>'
        ),
        "gunban": (
            '<emoji document_id=6334872157947955302>🤗</emoji> <b><a href="{}">{}</a>'
            " has been globally unbanned.</b>\n\n{}"
        ),
        "gunbanning": (
            "<emoji document_id=6334872157947955302>🤗</emoji> <b>Global unbanning <a"
            ' href="{}">{}</a>...</b>'
        ),
        "in_n_chats": (
            "<emoji document_id=5379568936218009290>👎</emoji> <b>Banned in {}"
            " chat(s)</b>"
        ),
        "unbanned_in_n_chats": (
            "<emoji document_id=5461129450341014019>✋️</emoji> <b>Unbanned in {}"
            " chat(s)</b>"
        ),
        "glmute": (
            '<emoji document_id=5301059317753979286>🖕</emoji> <b><a href="{}">{}</a>'
            " has been globally muted.</b>\n<b>Reason: </b><i>{}</i>\n\n{}"
        ),
        "glmutes": (
            "<emoji document_id=5301059317753979286>🖕</emoji> <b>Global mute <a"
            ' href="{}">{}</a>...</b>'
        ),
        "gunmute": (
            '<emoji document_id=6334872157947955302>🤗</emoji> <b><a href="{}">{}</a>'
            " has been globally unmuted.</b>\n\n{}"
        ),
        "gunmutes": (
            "<emoji document_id=6334872157947955302>🤗</emoji> <b>Global unmute <a"
            ' href="{}">{}</a>...</b>'
        ),
        "in_m_chats": (
            "<emoji document_id=5379568936218009290>👎</emoji> <b>Muted in {}"
            " chat(s)</b>"
        ),
        "unmute_in_n_chats": (
            "<emoji document_id=5461129450341014019>✋️</emoji> <b>Unmuted in {}"
            " chat(s)</b>"
        ),
    }

    strings_ru = {
        "no_reason": "Не указана",
        "args": (
            "<emoji document_id=5300759756669984376>🚫</emoji> <b>Неверные"
            " аргументы</b>"
        ),
        "glban": (
            '<emoji document_id=5301059317753979286>🖕</emoji> <b><a href="{}">{}</a>'
            " был гзабанен.</b>\n<b>Причина: </b><i>{}</i>\n\n{}"
        ),
        "glbanning": (
            "<emoji document_id=5301059317753979286>🖕</emoji> <b>Гбан <a"
            ' href="{}">{}</a>...</b>'
        ),
        "gunban": (
            '<emoji document_id=6334872157947955302>🤗</emoji> <b><a href="{}">{}</a>'
            " был гразбанен.</b>\n\n{}"
        ),
        "gunbanning": (
            "<emoji document_id=6334872157947955302>🤗</emoji> <b>Гразбан <a"
            ' href="{}">{}</a>...</b>'
        ),
        "in_n_chats": (
            "<emoji document_id=5379568936218009290>👎</emoji> <b>Забанил в {}"
            " чат(-ах)</b>"
        ),
        "unbanned_in_n_chats": (
            "<emoji document_id=5461129450341014019>✋️</emoji> <b>Разбанил in {}"
            " чат(-ах)</b>"
        ),
        "glmute": (
            '<emoji document_id=5301059317753979286>🖕</emoji> <b><a href="{}">{}</a>'
            " был замучен.</b>\n<b>Причина: </b><i>{}</i>\n\n{}"
        ),
        "glmutes": (
            "<emoji document_id=5301059317753979286>🖕</emoji> <b>Гмут <a"
            ' href="{}">{}</a>...</b>'
        ),
        "gunmute": (
            '<emoji document_id=6334872157947955302>🤗</emoji> <b><a href="{}">{}</a>'
            " был размучен.</b>\n\n{}"
        ),
        "gunmutes": (
            "<emoji document_id=6334872157947955302>🤗</emoji> <b>Гразмут <a"
            ' href="{}">{}</a>...</b>'
        ),
        "in_m_chats": (
            "<emoji document_id=5379568936218009290>👎</emoji> <b>Мут в {}"
            " чат(-ах)</b>"
        ),
        "unmute_in_n_chats": (
            "<emoji document_id=5461129450341014019>✋️</emoji> <b>Размут in {}"
            " чат(-ах)</b>"
        ),
    }

    def __init__(self):
        self._gban_cache = {}
        self._gmute_cache = {}

    @staticmethod
    def convert_time(t: str) -> int:
        """
        Tries to export time from text
        """
        try:
            if not str(t)[:-1].isdigit():
                return 0

            if "d" in str(t):
                t = int(t[:-1]) * 60 * 60 * 24

            if "h" in str(t):
                t = int(t[:-1]) * 60 * 60

            if "m" in str(t):
                t = int(t[:-1]) * 60

            if "s" in str(t):
                t = int(t[:-1])

            t = int(re.sub(r"[^0-9]", "", str(t)))
        except ValueError:
            return 0

        return t

    async def args_parser(
        self,
        message: Message,
        include_force: bool = False,
        include_silent: bool = False,
    ) -> tuple:
        """Get args from message"""
        args = " " + utils.get_args_raw(message)
        if include_force and " -f" in args:
            force = True
            args = args.replace(" -f", "")
        else:
            force = False

        if include_silent and " -s" in args:
            silent = True
            args = args.replace(" -s", "")
        else:
            silent = False

        args = args.strip()

        reply = await message.get_reply_message()

        if reply and not args:
            return (
                (await self._client.get_entity(reply.sender_id)),
                0,
                utils.escape_html(self.strings("no_reason")).strip(),
                *((force,) if include_force else []),
                *((silent,) if include_silent else []),
            )

        try:
            a = args.split()[0]
            if str(a).isdigit():
                a = int(a)
            user = await self._client.get_entity(a)
        except Exception:
            try:
                user = await self._client.get_entity(reply.sender_id)
            except Exception:
                return False

        t = ([arg for arg in args.split() if self.convert_time(arg)] or ["0"])[0]
        args = args.replace(t, "").replace("  ", " ")
        t = self.convert_time(t)

        if not reply:
            try:
                args = " ".join(args.split()[1:])
            except Exception:
                pass

        if time.time() + t >= 2208978000:  # 01.01.2040 00:00:00
            t = 0

        return (
            user,
            t,
            utils.escape_html(args or self.strings("no_reason")).strip(),
            *((force,) if include_force else []),
            *((silent,) if include_silent else []),
        )

    async def ban(
        self,
        chat: typing.Union[Chat, int],
        user: typing.Union[User, Channel, int],
        period: int = 0,
        reason: str = None,
        message: typing.Optional[Message] = None,
        silent: bool = False,
    ):
        """Ban user in chat"""
        if str(user).isdigit():
            user = int(user)

        if reason is None:
            reason = self.strings("no_reason")

        try:
            await self.inline.bot.kick_chat_member(
                int(f"-100{getattr(chat, 'id', chat)}"),
                int(getattr(user, "id", user)),
            )
        except Exception:
            logger.debug("Can't ban with bot", exc_info=True)

            await self._client.edit_permissions(
                chat,
                user,
                until_date=(time.time() + period) if period else 0,
                **BANNED_RIGHTS,
            )

        if silent:
            return

    async def mute(
        self,
        chat: typing.Union[Chat, int],
        user: typing.Union[User, Channel, int],
        period: int = 0,
        reason: str = None,
        message: typing.Optional[Message] = None,
        silent: bool = False,
    ):
        """Mute user in chat"""
        if str(user).isdigit():
            user = int(user)

        if reason is None:
            reason = self.strings("no_reason")

        try:
            await self.inline.bot.restrict_chat_member(
                int(f"-100{getattr(chat, 'id', chat)}"),
                int(getattr(user, "id", user)),
            )
        except Exception:
            logger.debug("Can't ban with bot", exc_info=True)

            await self._client.edit_permissions(
                chat,
                user,
                until_date=(time.time() + period) if period else 0,
                **MUTES_RIGHTS,
            )

        if silent:
            return

    @loader.command()
    async def glban(self, message):
        "<реплай | юзер> [причина] [-s] - Забанить пользователя во всех чатах где ты админ"

        reply = await message.get_reply_message()
        args = utils.get_args_raw(message)
        if not reply and not args:
            await utils.answer(message, self.strings("args"))
            return

        a = await self.args_parser(message, include_silent=True)

        if not a:
            await utils.answer(message, self.strings("args"))
            return

        user, t, reason, silent = a

        message = await utils.answer(
            message,
            self.strings("glbanning").format(
                utils.get_entity_url(user),
                utils.escape_html(get_full_name(user)),
            ),
        )

        if not self._gban_cache or self._gban_cache["exp"] < time.time():
            self._gban_cache = {
                "exp": int(time.time()) + 10 * 60,
                "chats": [
                    chat.entity.id
                    async for chat in self._client.iter_dialogs()
                    if (
                        (
                            isinstance(chat.entity, Chat)
                            or (
                                isinstance(chat.entity, Channel)
                                and getattr(chat.entity, "megagroup", False)
                            )
                        )
                        and chat.entity.admin_rights
                        and chat.entity.participants_count > 5
                        and chat.entity.admin_rights.ban_users
                    )
                ],
            }

        chats = ""
        counter = 0

        for chat in self._gban_cache["chats"]:
            try:
                await self.ban(chat, user, 0, reason, silent=True)
            except Exception:
                pass
            else:
                chats += '▫️ <b><a href="{}">{}</a></b>\n'.format(
                    utils.get_entity_url(await self._client.get_entity(chat, exp=0)),
                    utils.escape_html(
                        get_full_name(await self._client.get_entity(chat, exp=0))
                    ),
                )
                counter += 1

        await utils.answer(
            message,
            self.strings("glban").format(
                utils.get_entity_url(user),
                utils.escape_html(get_full_name(user)),
                reason,
                self.strings("in_n_chats").format(counter) if silent else chats,
            ),
        )

    @loader.command()
    async def glunban(self, message: Message):
        "<реплай | юзер> [причина] [-s] - Разбанить пользователя во всех где ты админ"

        reply = await message.get_reply_message()
        args = utils.get_args_raw(message)
        if not reply and not args:
            await utils.answer(message, self.strings("args"))
            return

        a = await self.args_parser(message, include_silent=True)

        if not a:
            await utils.answer(message, self.strings("args"))
            return

        user, t, reason, silent = a

        message = await utils.answer(
            message,
            self.strings("gunbanning").format(
                utils.get_entity_url(user),
                utils.escape_html(get_full_name(user)),
            ),
        )

        if not self._gban_cache or self._gban_cache["exp"] < time.time():
            self._gban_cache = {
                "exp": int(time.time()) + 10 * 60,
                "chats": [
                    chat.entity.id
                    async for chat in self._client.iter_dialogs()
                    if (
                        (
                            isinstance(chat.entity, Chat)
                            or (
                                isinstance(chat.entity, Channel)
                                and getattr(chat.entity, "megagroup", False)
                            )
                        )
                        and chat.entity.admin_rights
                        and chat.entity.participants_count > 5
                        and chat.entity.admin_rights.ban_users
                    )
                ],
            }

        chats = ""
        counter = 0

        for chat in self._gban_cache["chats"]:
            try:
                await self._client.edit_permissions(
                    chat,
                    user,
                    until_date=0,
                    **{right: True for right in BANNED_RIGHTS.keys()},
                )
            except Exception:
                pass
            else:
                chats += '▫️ <b><a href="{}">{}</a></b>\n'.format(
                    utils.get_entity_url(await self._client.get_entity(chat, exp=0)),
                    utils.escape_html(
                        get_full_name(await self._client.get_entity(chat, exp=0))
                    ),
                )
                counter += 1

        await utils.answer(
            message,
            self.strings("gunban").format(
                utils.get_entity_url(user),
                utils.escape_html(get_full_name(user)),
                (
                    self.strings("unbanned_in_n_chats").format(counter)
                    if silent
                    else chats
                ),
            ),
        )

    @loader.command()
    async def glmute(self, message):
        "<реплай | юзер> [причина] [-s] - Замутить пользователя во всех чатах где ты админ"

        reply = await message.get_reply_message()
        args = utils.get_args_raw(message)
        if not reply and not args:
            await utils.answer(message, self.strings("args"))
            return

        a = await self.args_parser(message, include_silent=True)

        if not a:
            await utils.answer(message, self.strings("args"))
            return

        user, t, reason, silent = a

        message = await utils.answer(
            message,
            self.strings("glmutes").format(
                utils.get_entity_url(user),
                utils.escape_html(get_full_name(user)),
            ),
        )

        if not self._gmute_cache or self._gmute_cache["exp"] < time.time():
            self._gmute_cache = {
                "exp": int(time.time()) + 10 * 60,
                "chats": [
                    chat.entity.id
                    async for chat in self._client.iter_dialogs()
                    if (
                        (
                            isinstance(chat.entity, Chat)
                            or (
                                isinstance(chat.entity, Channel)
                                and getattr(chat.entity, "megagroup", False)
                            )
                        )
                        and chat.entity.admin_rights
                        and chat.entity.participants_count > 5
                        and chat.entity.admin_rights.ban_users
                    )
                ],
            }

        chats = ""
        counter = 0

        for chat in self._gmute_cache["chats"]:
            try:
                await self.mute(chat, user, 0, reason, silent=True)
            except Exception:
                pass
            else:
                chats += '▫️ <b><a href="{}">{}</a></b>\n'.format(
                    utils.get_entity_url(await self._client.get_entity(chat, exp=0)),
                    utils.escape_html(
                        get_full_name(await self._client.get_entity(chat, exp=0))
                    ),
                )
                counter += 1

        await utils.answer(
            message,
            self.strings("glmute").format(
                utils.get_entity_url(user),
                utils.escape_html(get_full_name(user)),
                reason,
                self.strings("in_m_chats").format(counter) if silent else chats,
            ),
        )

    @loader.command()
    async def glunmute(self, message: Message):
        "<реплай | юзер> [причина] [-s] - Размутит пользователя во всех где ты админ"

        reply = await message.get_reply_message()
        args = utils.get_args_raw(message)
        if not reply and not args:
            await utils.answer(message, self.strings("args"))
            return

        a = await self.args_parser(message, include_silent=True)

        if not a:
            await utils.answer(message, self.strings("args"))
            return

        user, t, reason, silent = a

        message = await utils.answer(
            message,
            self.strings("gunmutes").format(
                utils.get_entity_url(user),
                utils.escape_html(get_full_name(user)),
            ),
        )

        if not self._gmute_cache or self._gmute_cache["exp"] < time.time():
            self._gmute_cache = {
                "exp": int(time.time()) + 10 * 60,
                "chats": [
                    chat.entity.id
                    async for chat in self._client.iter_dialogs()
                    if (
                        (
                            isinstance(chat.entity, Chat)
                            or (
                                isinstance(chat.entity, Channel)
                                and getattr(chat.entity, "megagroup", False)
                            )
                        )
                        and chat.entity.admin_rights
                        and chat.entity.participants_count > 5
                        and chat.entity.admin_rights.ban_users
                    )
                ],
            }

        chats = ""
        counter = 0

        for chat in self._gmute_cache["chats"]:
            try:
                await self._client.edit_permissions(
                    chat,
                    user,
                    until_date=0,
                    **{right: True for right in MUTES_RIGHTS.keys()},
                )
            except Exception:
                pass
            else:
                chats += '▫️ <b><a href="{}">{}</a></b>\n'.format(
                    utils.get_entity_url(await self._client.get_entity(chat, exp=0)),
                    utils.escape_html(
                        get_full_name(await self._client.get_entity(chat, exp=0))
                    ),
                )
                counter += 1

        await utils.answer(
            message,
            self.strings("gunmute").format(
                utils.get_entity_url(user),
                utils.escape_html(get_full_name(user)),
                (
                    self.strings("unmutes_in_n_chats").format(counter)
                    if silent
                    else chats
                ),
            ),
        )
