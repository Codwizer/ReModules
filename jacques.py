# ---------------------------------------------------------------------------------
# Name: Жаконизатор
# Description: Жаконизатор
# Author: @hikka_mods
# ---------------------------------------------------------------------------------

# 🔒    Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# meta developer: @hikka_mods
# scope: Жаконизатор
# scope: Жаконизатор 0.0.1
# ---------------------------------------------------------------------------------

import io, requests
from textwrap import wrap

from PIL import Image, ImageDraw, ImageFont

from .. import loader, utils

__version__ = (1, 0, 0)


@loader.tds
class JacquesMod(loader.Module):
    """Жаконизатор"""

    strings = {"name": "Жаконизатор", "usage": "Write <code>.help Жаконизатор</code>"}

    strings_ru = {"usage": "Напиши <code>.help Жаконизатор</code>"}

    def __init__(self):
        self.name = self.strings["name"]
        self._me = None
        self._ratelimit = []
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "font",
                "https://github.com/Codwizer/ReModules/blob/main/assets/OpenSans-Light.ttf?raw=true",
                lambda: "добавьте ссылку на нужный вам шрифт",
            ),
            loader.ConfigValue(
                "location",
                "center",
                "Можно указать left, right или center",
                validator=loader.validators.Choice(["left", "right", "center"]),
            ),
        )

    async def ionicmd(self, message):
        """<реплай на сообщение/свой текст>"""
        ufr = requests.get(self.config["font"]).content
        f = ufr

        reply = await message.get_reply_message()
        args = utils.get_args_raw(message)
        if not args:
            if not reply:
                await utils.answer(message, self.strings("usage", message))
                return
            else:
                txt = reply.raw_text
        else:
            txt = utils.get_args_raw(message)
        pic = requests.get(
            "https://raw.githubusercontent.com/Codwizer/ReModules/main/assets/IMG_20231128_152538.jpg"
        )
        pic.raw.decode_content = True
        img = Image.open(io.BytesIO(pic.content)).convert("RGB")

        W, H = img.size
        text = "\n".join(wrap(txt, 19))
        t = text + "\n"
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype(io.BytesIO(f), 32, encoding="UTF-8")
        w, h = draw.multiline_textsize(t, font=font)
        imtext = Image.new("RGBA", (w + 10, h + 10), (0, 0, 0, 0))
        draw = ImageDraw.Draw(imtext)
        draw.multiline_text(
            (10, 10), t, (0, 0, 0), font=font, align=self.config["location"]
        )
        imtext.thumbnail((350, 195))
        w, h = 350, 195
        img.paste(imtext, (10, 10), imtext)
        out = io.BytesIO()
        out.name = "hikka_mods.jpg"
        img.save(out)
        out.seek(0)
        await message.client.send_file(message.to_id, out, reply_to=reply)
        await message.delete()
