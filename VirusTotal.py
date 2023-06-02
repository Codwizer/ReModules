# ---------------------------------------------------------------------------------
# Name: VirusTotal
# Description: Checks files for viruses using VirusTotal
# Author: @re_modules
# ---------------------------------------------------------------------------------

# 🔒    Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# meta developer: @re_modules
# scope: Api VirusTotal
# scope: Api VirusTotal 0.0.1
# requires: json requests
# ---------------------------------------------------------------------------------

import os, json, requests
from .. import loader, utils
from hikkatl.types import Message

def register(cb):
    cb(VirusMod())

class VirusTotalMod(loader.Module):
    strings = {
    "name": "VirusTotal",
    "no_file": "You have not selected a file",
    "download": "Downloading...",
    "skan": "Scanning...",
    "link": "🦠 Link to VirusTotal",
    "no_virus": "✅ The file is clean",
    "error": "Scan error.",
    "no_format": "This format is not supported."
    }
    
    strings_ru = {
    "no_file": "Вы не выбрали файл.",
    "download": "Скачивание...",
    "skan": "Сканирую...",
    "link": "🦠 Ссылка на VirusTotal",
    "no_virus": "✅ Файл чист.",
    "error": "Ошибка сканирования.",
    "no_format": "Этот формат не поддерживается."
    }



    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
            "token-vt",
            "No token",
            "Need a token with www.virustotal.com/gui/my-apikey",
            )
         )

    async def vtcmd(self, message: Message):
        """<response to the file> - Checks files for viruses using VirusTotal"""
        fil = ""
        reply = await message.get_reply_message()
        if not reply:
            await utils.answer(message, self.strings("no_file"))
            return
        else:
            for i in os.listdir():
                if "file" in i:
                    os.system(f"rm -rf {i}")
            await utils.answer(message, self.strings("download"))
            await reply.download_media('file')
            for i in os.listdir():
                if "file" in i:
                    fil = i
            if not fil:
                await utils.answer(message, self.strings("no_file"))
                return
            await utils.answer(message, self.strings("skan")) 
            if fil not in ["file.jpg", "file.png", "file.ico", "file.mp3", "file.mp4", "file.gif", "file.txt"]: 
                token = self.config["token-vt"]
                params = dict(apikey = token)
                with open(fil, 'rb') as file:
                    files = dict(file=(fil, file))
                    response = requests.post('https://www.virustotal.com/vtapi/v2/file/scan', files=files, params=params)
                os.system(f"rm -rf {fil}")
                try:
                    if response.status_code == 200:
                        false = []
                        result=response.json()
                        res = (json.dumps(result, sort_keys=False, indent=4)).split()[10].split('"')[1]
                        params = dict(apikey = token, resource=res)
                        response = requests.get('https://www.virustotal.com/vtapi/v2/file/report', params=params)
                        if response.status_code == 200:
                            result = response.json()
                            for key in result['scans']:
                                if result['scans'][key]['detected']:
                                    false.append(f"⛔️ <b>{key}</b>\n ╰ <code>{result['scans'][key]['result']}</code>")
                            out = '\n'.join(false) if len(false) > 0 else self.strings("no_virus")
                            uyrl = f"https://www.virustotal.com/gui/file/{result['resource']}/detection"
                            await self.inline.form(
                                text=f"Detections: {len(false)} / {len(result['scans'])}\n\n{out}\n\n",
                                message=message,
                                reply_markup={
                                     "text": self.strings("link"),
                                     "url": uyrl,
                                },
                            )
                except:
                    await utils.answer(message, self.strings("error"))
            else:
                await utils.answer(message, self.strings("no_format"))
                os.system(f"rm -rf {fil}")