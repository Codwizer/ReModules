# ---------------------------------------------------------------------------------
# Name: NumbersAPI
# Description: Many interesting facts about numbers. Idea @FurryMods
# Author: @hikka_mods
# ---------------------------------------------------------------------------------

# 🔒    Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# meta developer: @hikka_mods
# scope: NumbersAPI
# scope: NumbersAPI 0.0.1
# ---------------------------------------------------------------------------------

from hikkatl.types import Message
from .. import loader, utils
import requests
from datetime import datetime

__version__ = (1, 0, 0)


def get_fact_about_number(number, fact_type):
    url = f"http://numbersapi.com/{number}/{fact_type}"
    response = requests.get(url)

    if response.status_code == 200:
        return response.text
    else:
        return "Извините, не удалось получить факт."


def get_fact_about_date(month, day):
    date_str = datetime.now().replace(month=month, day=day).strftime("%m/%d")
    url = f"http://numbersapi.com/{date_str}/date"
    response = requests.get(url)

    if response.status_code == 200:
        return response.text
    else:
        return "Извините, не удалось получить факт."


@loader.tds
class NumbersAPI(loader.Module):
    """Many interesting facts about numbers. idea @FurryMods"""

    strings = {"name": "NumbersAPI"}

    async def numcmd(self, message: Message):
        """Дает интересный факт про число или дату\nНапример: .num 10 math или .num 01.01 date"""
        args = utils.get_args_raw(message).split()

        if len(args) >= 2:
            num_or_date = args[0]
            fact_type = args[1]
            if "." in num_or_date:
                month, day = map(int, num_or_date.split("."))
                result = get_fact_about_date(month, day)
            else:
                number = int(num_or_date)
                result = get_fact_about_number(number, fact_type)
            await utils.answer(message, f"{result}")
        else:
            await utils.answer(message, "Использование: .num <число или дата> <тип>")
