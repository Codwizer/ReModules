
#              © Copyright 2023
#           https://t.me/Re_Modules
#
#        Licensed under the GNU AGPLv3
#   https://www.gnu.org/licenses/agpl-3.0.html

# requires: json requests
import os, json, requests
from .. import loader, utils
from hikkatl.types import Message

def register(cb):
    cb(VirusMod())

class VirusMod(loader.Module):
    strings = {'name': 'VirusTotal'}
     
    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
            "token-vt",
            "No token",
            "Нужен токен с www.virustotal.com/gui/my-apikey",
            )
         )

    async def vtcmd(self, message: Message):
        """Проверяет файлы на наличие вирусов с помощью VirusTotal"""
        fil = ""
        reply = await message.get_reply_message()
        if not reply:
            await utils.answer(message, "<b>Вы не выбрали файл.</b>")
            return
        else:
            for i in os.listdir():
                if "file" in i:
                    os.system(f"rm -rf {i}")
            await utils.answer(message, "<b>Скачивание...</b>")
            await reply.download_media('file')
            for i in os.listdir():
                if "file" in i:
                    fil = i
            if not fil:
                await utils.answer(message, "<b>You did not select the file.</b>")
                return
            await utils.answer(message, "<b>Сканирование...</b>") 
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
                            out = '\n'.join(false) if len(false) > 0 else '<b>✅ Файл чист.</b>'
                            uyrl = f"https://www.virustotal.com/gui/file/{result['resource']}/detection"
                            await self.inline.form(
                                text=f"🧬 Обнаружения: {len(false)} / {len(result['scans'])}\n\n{out}\n\n",
                                message=message,
                                reply_markup={
                                     "text": "🦠 Ссылка на VirusTotal",
                                     "url": uyrl,
                                },
                            )
                except:
                    await utils.answer(message, "<b>Ошибка сканирования.</b>")
            else:
                await utils.answer(message, "<b>Этот формат не поддерживается.</b>")
                os.system(f"rm -rf {fil}")
