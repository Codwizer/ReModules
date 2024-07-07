import requests
from hikkatl.types import Message
from .. import loader, utils


def get_creation_date(id: int) -> str:
    url = "https://restore-access.indream.app/regdate"
    headers = {
        "accept": "*/*",
        "content-type": "application/x-www-form-urlencoded",
        "user-agent": "Nicegram/92 CFNetwork/1390 Darwin/22.0.0",
        "x-api-key": "e758fb28-79be-4d1c-af6b-066633ded128",
        "accept-language": "en-US,en;q=0.9",
    }
    data = {"telegramId": id}
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["data"]["date"]
    else:
        return "Ошибка получения данных"


@loader.tds
class AccountData(loader.Module):
    """Find out the approximate date of registration of the telegram account"""

    strings = {
        "name": "AccountData", 
        "date_text": "🕰 Date of registration of this account: {data}",
        "date_text_ps": "P.S. The registration date is approximate, as it is almost impossible to know for sure",
        "no_reply": "⚠️ You did not reply to the user's message",
    }

    strings_ru = {
        "date_text": "🕰 Дата регистрации этого аккаунта: {data}",
        "date_text_ps": "P.S. Дата регистрации примерная, так как точно узнать практически невозможно",
        "no_reply": "⚠️ Вы не ответили на сообщение пользователя",
    }

    async def accdatacmd(self, message: Message):
        """Узнать примерную дату регистрации аккаунта телеграмм"""

        reply = await message.get_reply_message()
        if reply:
            data = get_creation_date(reply.from_id)
            await utils.answer(message, f"{self.strings('date_text').format(data=data)}\n\n{self.strings('date_text_ps')}")
        else:
            await utils.answer(message, self.strings("no_reply"))
