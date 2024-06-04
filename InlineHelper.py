# ---------------------------------------------------------------------------------
# Name: InlineHelper
# Description: Basic management of the UB in case only the inline works
# Author: @hikka_mods
# ---------------------------------------------------------------------------------

# 🔒    Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# meta developer: @hikka_mods
# scope: InlineHelper
# scope: InlineHelper 0.0.1
# ---------------------------------------------------------------------------------
import sys
import os
import asyncio
import logging
from .. import loader, utils, main

from ..inline.types import InlineCall, InlineQuery


class InlineHelperMod(loader.Module):
    """Basic management of the UB in case only the inline works"""

    strings = {
        "name": "InlineHelper",
        "call_restart": "Restarting...",
        "call_update": "Updating...",
        "res_prefix": "Successfully reset prefix to default",
        "restart_inline_handler_title": "Restart Userbot",
        "restart_inline_handler_description": "Restart your userbot via inline",
        "restart_inline_handler_message": "Press the button below to restart your userbot",
        "restart_inline_handler_reply_text": "Restart",
        "update_inline_handler_title": "Update Userbot",
        "update_inline_handler_description": "Update your userbot via inline",
        "update_inline_handler_message": "Press the button below to update your userbot",
        "update_inline_handler_reply_text": "Update",
        "terminal_inline_handler_title": "Command Executed!",
        "terminal_inline_handler_description": "Command executed successfully",
        "terminal_inline_handler_message": "Command {text} executed successfully in terminal",
        "modules_inline_handler_title": "Modules",
        "modules_inline_handler_description": "List all installed modules",
        "modules_inline_handler_result": "☘️ Installed modules:\n",
        "resetprefix_inline_handler_title": "Reset Prefix",
        "resetprefix_inline_handler_description": "Reset your prefix back to default",
        "resetprefix_inline_handler_message": "Are you sure you want to reset your prefix to default dot?",
        "resetprefix_inline_handler_reply_text_yes": "Yes",
        "resetprefix_inline_handler_reply_text_no": "No",
    }

    strings_ru = {
        "call_restart": "Перезагружаю...",
        "call_update": "Обновляю...",
        "res_prefix": "Префикс успешно сброшен по умолчанию",
        "restart_inline_handler_title": "Перезагрузить юзербота",
        "restart_inline_handler_description": "Перезагрузить юзербота через инлайн",
        "restart_inline_handler_message": "<b>Нажмите на кнопку ниже для рестарта юзербота</b>",
        "restart_inline_handler_reply_text": "Перезапуск",
        "update_inline_handler_title": "Обновить юзербота",
        "update_inline_handler_description": "Обновить юзербота через инлайн",
        "update_inline_handler_message": "<b>Нажмите на кнопку ниже для обновления юзербота</b>",
        "update_inline_handler_reply_text": "Обновить",
        "terminal_inline_handler_title": "Команда выполнена!",
        "terminal_inline_handler_description": "Команда завершена.",
        "terminal_inline_handler_message": "Команда <code>{text}</code> была успешно выполнена в терминале",
        "modules_inline_handler_title": "Модули",
        "modules_inline_handler_description": "Вывести список установленных моудей",
        "modules_inline_handler_result": "☘️ Все установленные модули:\n",
        "resetprefix_inline_handler_title": "Сбросить префикс",
        "resetprefix_inline_handler_description": "Сбросить префикс по умолчанию",
        "resetprefix_inline_handler_message": "Вы действительно хотите сбросить ваш префикс и установить стандартную точку?",
        "resetprefix_inline_handler_reply_text_yes": "Да",
        "resetprefix_inline_handler_reply_text_no": "Нет",
    }

    async def client_ready(self, client, db):
        self.client = client
        self.db = db

    async def restart(self, call):
        """Restart callback"""
        logging.error("InlineHelper: restarting userbot...")
        await call.edit(self.strings("call_restart"))
        await sys.exit(0)

    async def update(self, call):
        """Update callback"""
        logging.error("InlineHelper: updating userbot...")
        os.system(f"cd {utils.get_base_dir()} && cd .. && git reset --hard HEAD")
        os.system("git pull")
        await call.edit(self.strings("call_update"))
        await sys.exit(0)

    async def reset_prefix(self, call):
        """Reset prefix"""
        self.db.set(main.__name__, "command_prefix", ".")
        await call.edit(self.strings("res_prefix"))

    async def restart_inline_handler(self, query: InlineQuery):
        """- перезагрузить юзербота"""

        return {
            "title": self.strings("restart_inline_handler_title"),
            "description": self.strings("restart_inline_handler_description"),
            "message": self.strings("restart_inline_handler_message"),
            "reply_markup": [
                {
                    "text": self.strings("restart_inline_handler_reply_text"),
                    "callback": self.restart,
                }
            ],
        }

    async def update_inline_handler(self, query: InlineQuery):
        """- обновить юзербота"""

        return {
            "title": self.strings("update_inline_handler_title"),
            "description": self.strings("update_inline_handler_description"),
            "message": self.strings("update_inline_handler_message"),
            "reply_markup": [
                {
                    "text": self.strings("update_inline_handler_reply_text"),
                    "callback": self.update,
                }
            ],
        }

    async def terminal_inline_handler(self, query: InlineQuery):
        """- выполнить команду в терминале (лучше сразу подготовить команду и просто вставить)"""

        text = query.args

        sproc = await asyncio.create_subprocess_shell(
            f"{text}",
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=utils.get_base_dir(),
        )

        return {
            "title": self.strings("terminal_inline_handler_title"),
            "description": self.strings("terminal_inline_handler_description"),
            "message": self.strings("terminal_inline_handler_message").format(
                text=text
            ),
        }

    async def modules_inline_handler(self, query: InlineQuery):
        """- вывести список установленных модулей через инлайн"""

        result = self.strings("modules_inline_handler_result")

        for mod in self.allmodules.modules:
            try:
                name = mod.strings["name"]
            except KeyError:
                name = mod.__clas__.__name__
            result += f"• {name}\n"

        return {
            "title": self.strings("modules_inline_handler_title"),
            "description": self.strings("modules_inline_handler_description"),
            "message": result,
        }

    async def resetprefix_inline_handler(self, query: InlineQuery):
        """- сбросить префикс (осторожнее, сбрасывает ваш префикс на . )"""

        return {
            "title": self.strings("resetprefix_inline_handler_title"),
            "description": self.strings("resetprefix_inline_handler_description"),
            "message": self.strings("resetprefix_inline_handler_message"),
            "reply_markup": [
                {
                    "text": self.strings("resetprefix_inline_handler_reply_text_yes"),
                    "callback": self.reset_prefix,
                },
                {
                    "text": self.strings("resetprefix_inline_handler_reply_text_no"),
                    "action": "close",
                },
            ],
        }
