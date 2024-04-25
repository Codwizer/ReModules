# ---------------------------------------------------------------------------------
# Name: VirusTotal
# Description: Checks files for viruses using VirusTotal
# Author: @hikka_mods
# ---------------------------------------------------------------------------------
# 🔒    Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# meta developer: @hikka_mods
# scope: Api VirusTotal
# scope: Api VirusTotal 0.0.1
# requires: json aiohttp tempfile
# ---------------------------------------------------------------------------------

import os, json, aiohttp, tempfile
from .. import loader, utils
from hikkatl.tl.types import Message

__version__ = (1, 0, 0)


@loader.tds
class VirusTotalMod(loader.Module):
    """Checks files for viruses using VirusTotal"""

    strings = {
        "name": "VirusTotal",
        "no_file": "<emoji document_id=5210952531676504517>🚫</emoji> </b>You haven't selected a file.</b>",
        "download": (
            "<emoji document_id=5334677912270415274>😑</emoji> </b>Downloading...</b>"
        ),
        "skan": "<emoji document_id=5325792861885570739>🫥</emoji>  <b>Scanning...</b>",
        "link": "🦠 VirusTotal Link",
        "no_virus": "✅ File is clean.",
        "error": "Scan error.",
        "no_format": "This format is not supported.",
        "no_apikey": (
            "<emoji document_id=5260342697075416641>🚫</emoji> You have not specified an API Key"
        ),
    }

    strings_ru = {
        "no_file": "<emoji document_id=5210952531676504517>🚫</emoji> </b>Вы не выбрали файл.</b>",
        "download": (
            "<emoji document_id=5334677912270415274>😑</emoji> </b>Скачивание...</b>"
        ),
        "skan": "<emoji document_id=5325792861885570739>🫥</emoji>  <b>Сканирую...</b>",
        "link": "🦠 Ссылка на VirusTotal",
        "no_virus": "✅ Файл чист.",
        "error": "Ошибка сканирования.",
        "no_format": "Этот формат не поддерживается.",
        "no_apikey": (
            "<emoji document_id=5260342697075416641>🚫</emoji> Вы не указали Api Key"
        ),
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "token-vt",
                None,
                lambda: "Need a token with www.virustotal.com/gui/my-apikey",
                validator=loader.validators.Hidden(),
            )
        )

    @loader.command()
    async def vt(self, message: Message):
        """<ответ на файл> - Проверяет файлы на наличие вирусов с использованием VirusTotal"""
        if not message.is_reply:
            await utils.answer(message, self.strings("no_reply"))
            return

        reply = await message.get_reply_message()
        if not reply.document:
            await utils.answer(message, self.strings("reply_not_document"))
            return

        if not self.config.get("token-vt"):
            await utils.answer(message, self.strings("no_apikey"))
            return

        async with aiohttp.ClientSession() as session:
            with tempfile.TemporaryDirectory() as temp_dir:
                await utils.answer(message, self.strings("download"))
                file_path = os.path.join(temp_dir, reply.file.name)
                await reply.download_media(file_path)

                file_extension = os.path.splitext(reply.file.name)[1].lower()
                allowed_extensions = (
                    ".jpg",
                    ".png",
                    ".ico",
                    ".mp3",
                    ".mp4",
                    ".gif",
                    ".txt",
                )

                if file_extension not in allowed_extensions:
                    try:
                        token = self.config["token-vt"]
                        headers = {"x-apikey": token}
                        params = {"apikey": token}

                        # Отправляем файл на сканирование
                        with open(file_path, "rb") as file:
                            files = {"file": file}
                            async with session.post(
                                "https://www.virustotal.com/api/v3/files",
                                headers=headers,
                                params=params,
                                data=files,
                            ) as response:
                                if response.status == 200:
                                    result = await response.json()
                                    data_id = result["data"]["id"]

                                    # Получаем отчет о сканировании
                                    async with session.get(
                                        f"https://www.virustotal.com/api/v3/analyses/{data_id}",
                                        headers=headers,
                                        params=params,
                                    ) as response:
                                        if response.status == 200:
                                            result = await response.json()
                                            hash = result["meta"]["file_info"]["sha256"]
                                            detections = []
                                            for engine, details in result["data"][
                                                "attributes"
                                            ]["results"].items():
                                                if details["category"] == "malicious":
                                                    detections.append(
                                                        f"⛔️ <b>{engine}</b>\n ╰ <code>{details['result']}</code>"
                                                    )
                                            out = (
                                                "\n".join(detections)
                                                if detections
                                                else self.strings("no_virus")
                                            )
                                            url = f"https://www.virustotal.com/gui/file/{hash}/detection"
                                            await self.inline.form(
                                                text=f"Detections: {len(detections)} / {len(result['data']['attributes']['results'])}\n\n{out}\n\n",
                                                message=message,
                                                reply_markup={
                                                    "text": self.strings("link"),
                                                    "url": url,
                                                },
                                            )
                    except Exception as e:
                        await utils.answer(
                            message,
                            self.strings("error") + f"\n\n{type(e).__name__}: {str(e)}",
                        )
                else:
                    await utils.answer(message, self.strings("no_format"))
