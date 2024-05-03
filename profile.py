# Name: Profile
# Description: Module for changing profile data.
# Author: @nervousmods
# Commands:
# .name | .about | .user
# ---------------------------------------------------------------------------------
# 🔒 Licensed under the GNU GPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html
# ⚠️ All modules is not scam and absolutely safe.
# 👤 https://t.me/smlgwy
# -----------------------------------------------------------------------------------
# meta developer: @nervousmods, @hikka_mods
# scope: hikka_only
# scope: hikka_min 1.5.0
# -----------------------------------------------------------------------------------

__version__ = (1, 0, 1)

from telethon.errors.rpcerrorlist import UsernameOccupiedError
from telethon.tl.functions.account import (
    UpdateProfileRequest,
    UpdateUsernameRequest,
)
from .. import loader, utils


@loader.tds
class ProfileEditorMod(loader.Module):
    """This module can change your Telegram profile."""

    strings = {
        "name": "Profile",
        "error_format": "Incorrect format of args. Try again.",
        "done_name": "The new name was successfully unstalled!",
        "done_bio": "The new bio was successfully unstaled!",
        "done_username": "The new username was succesfully installed!",
        "error_occupied": "The new username is already occupied!",
    }

    strings_ru = {
        "error_format": "Неправильный формат аргумента. Попробуйте еще раз.",
        "done_name": "Новое имя успешно настроено!",
        "done_bio": "Новое био успешно настроено!",
        "done_username": "Новое имя пользователя успешно установлено!",
        "error_occupied": "Новое имя пользователя уже занято!",
    }

    async def namecmd(self, message):
        """- for change your first/second name."""
        args = utils.get_args_raw(message).split("/")

        if len(args) == 0:
            return await utils.answer(message, self.strings("error_format"))
        if len(args) == 1:
            firstname = args[0]
            lastname = " "
        elif len(args) == 2:
            firstname = args[0]
            lastname = args[1]
        await message.client(
            UpdateProfileRequest(first_name=firstname, last_name=lastname)
        )
        await utils.answer(message, self.strings("done_name"))

    async def aboutcmd(self, message):
        """- for change your bio."""
        args = utils.get_args_raw(message)
        if not args:
            return await utils.answer(message, self.strings("error_format"))
        await message.client(UpdateProfileRequest(about=args))
        await utils.answer(message, self.strings("done_bio"))

    async def usercmd(self, message):
        """- for change your username. Enter value without "@"."""
        args = utils.get_args_raw(message)
        if not args:
            return await utils.answer(message, self.strings("error_format"))
        try:
            await message.client(UpdateUsernameRequest(args))
            await utils.answer(message, self.strings("done_username"))
        except UsernameOccupiedError:
            await utils.answer(message, self.strings("error_occupied"))
