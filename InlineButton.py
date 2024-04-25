# ---------------------------------------------------------------------------------
# Name: InlineButton
# Description: Create inline button
# Author: @hikka_mods
# ---------------------------------------------------------------------------------

# 🔒    Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# meta developer: @hikka_mods
# scope: InlineButton
# scope: InlineButton 0.0.1
# ---------------------------------------------------------------------------------
import asyncio
from ..inline.types import InlineQuery
from ..utils import rand
from .. import loader, utils

__version__ = (1, 0, 0)


@loader.tds
class InlineButtonMod(loader.Module):
    """Create inline button"""

    strings = {
        "name": "InlineButton",
        "titles": "Create a message with the Inline Button"
    }

    strings_ru = {
        "titles": "Создай сообщение с Inline Кнопкой"
    }

    async def crinl_inline_handler(self, query: InlineQuery):
        """- создать inline кнопку\nНапример: @username_bot crinl Текст сообщения, Текст кнопки, Ссылка в кнопке"""

        args = utils.get_args_raw(query.query)
        if args:
            args_list = args.split(",")
            if len(args_list) == 3:
                message = args_list[0].strip()
                name = args_list[1].strip()
                url = args_list[2].strip()

            return {
                "title": self.strings("titles"),
                "description": f"{message}, {name}, {url}",
                "message": message,
                "reply_markup": [{"text": name, "url": url}],
            }
