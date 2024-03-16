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
# requires: json, aiohttp, tempfile
# ---------------------------------------------------------------------------------

import os, json, aiohttp, tempfile
from .. import loader, utils
from hikkatl.tl.types import Message


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
        """<response to the file> - Checks files for viruses using VirusTotal"""
        reply = await message.get_reply_message()
        if not reply:
            await utils.answer(message, self.strings("no_file"))
            return

        if self.config["token-vt"] is None:
            await utils.answer(message, self.strings("no_apikey"))
            return

        async with aiohttp.ClientSession() as session:
            with tempfile.TemporaryDirectory() as temp_dir:
                await utils.answer(message, self.strings("download"))
                file_path = os.path.join(temp_dir, reply.file.name)
                await reply.download_media(file_path)

                await utils.answer(message, self.strings("skan"))
                file_name = os.path.basename(file_path)

                if file_name not in [
                    "file.jpg",
                    "file.png",
                    "file.ico",
                    "file.mp3",
                    "file.mp4",
                    "file.gif",
                    "file.txt",
                ]:
                    token = self.config["token-vt"]
                    params = dict(apikey=token)

                    try:
                        with open(file_path, "rb") as file:
                            files = {"file": (file_name, file)}
                            data = aiohttp.FormData()
                            data.add_field("file", file, filename=file_name)
                            async with session.post(
                                "https://www.virustotal.com/vtapi/v2/file/scan",
                                data=data,
                                params=params,
                            ) as response:
                                if response.status == 200:
                                    false = []
                                    result = await response.json()
                                    res = (
                                        (json.dumps(result, sort_keys=False, indent=4))
                                        .split()[10]
                                        .split('"')[1]
                                    )
                                    params = {"apikey": token, "resource": res}
                                    async with session.get(
                                        "https://www.virustotal.com/vtapi/v2/file/report",
                                        params=params,
                                    ) as response:
                                        if response.status == 200:
                                            result = await response.json()
                                            for key in result["scans"]:
                                                if result["scans"][key]["detected"]:
                                                    false.append(
                                                        f"⛔️ <b>{key}</b>\n ╰ <code>{result['scans'][key]['result']}</code>"
                                                    )
                                            out = (
                                                "\n".join(false)
                                                if len(false) > 0
                                                else self.strings("no_virus")
                                            )
                                            uyrl = f"https://www.virustotal.com/gui/file/{result['resource']}/detection"
                                            await self.inline.form(
                                                text=f"Detections: {len(false)} / {len(result['scans'])}\n\n{out}\n\n",
                                                message=message,
                                                reply_markup={
                                                    "text": self.strings("link"),
                                                    "url": uyrl,
                                                },
                                            )
                                        else:
                                            await utils.answer(
                                                message, self.strings("error")
                                            )
                                else:
                                    await utils.answer(message, self.strings("error"))
                    except Exception as e:
                        await utils.answer(
                            message,
                            self.strings("error") + f"\n\n{type(e).__name__}: {str(e)}",
                        )
                else:
                    await utils.answer(message, self.strings("no_format"))
