# ---------------------------------------------------------------------------------
# Name: SafetyMod
# Description: generate random password
# Author: @hikka_mods
# ---------------------------------------------------------------------------------

# 🔒    Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# meta developer: @hikka_mods
# scope: Api SafetyMod
# scope: Api SafetyMod 0.0.1
# ---------------------------------------------------------------------------------
import random
from telethon.tl.types import Message

from .. import loader, utils

__version__ = (1, 0, 0)


def generate_password(length, letters=True, numbers=True, symbols=True):
    """Function to generate random password"""
    LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    NUMBERS = "0123456789"
    SYMBOLS = "!#$%&*+-=?@^_"
    charsets = []
    if letters:
        charsets.append(LETTERS)
    if numbers:
        charsets.append(NUMBERS)
    if symbols:
        charsets.append(SYMBOLS)
    if not charsets:
        raise ValueError("At least one of letters, numbers, or symbols must be True")
    charset = "".join(charsets)
    password = "".join(random.choice(charset) for i in range(length))
    return password


class SafetyMod(loader.Module):
    """generate random password"""

    strings = {
        "name": "Safety",
        "pass": "<emoji document_id=5472287483318245416>*⃣</emoji> <b>Here is your secure password:</b> <code>{}</code>",
    }
    strings_ru = {
        "pass": "<emoji document_id=5472287483318245416>*⃣</emoji> <b>Вот ваш безопасный пароль:</b> <code>{}</code>"
    }

    async def passwordcmd(self, message):
        """random password\n-n - numbers\n-s - symbols \n -l - letters"""
        text = message.text.split()
        length = 10
        letters = True
        numbers = False
        symbols = False
        for i in text:
            if i.startswith("password"):
                length = int(i.split("password")[1])
            elif i == "-n":
                numbers = True
            elif i == "-s":
                symbols = True
            elif i == "-l":
                letters = True
        password = generate_password(
            length=length, letters=letters, numbers=numbers, symbols=symbols
        )
        await utils.answer(message, self.strings("pass").format(password))
