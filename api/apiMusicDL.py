# ---------------------------------------------------------------------------------
# Name: Api MusicDL
# Description: Help with moderation chat
# Author: @re_modules
# ---------------------------------------------------------------------------------

# 🔒    Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# meta developer: @re_modules
# scope: Api MusicDL
# scope: Api MusicDL 0.0.1
# ---------------------------------------------------------------------------------

import asyncio
import io
import logging
import typing

import requests
from telethon.errors.rpcerrorlist import BotResponseTimeoutError
from telethon.events import MessageEdited, StopPropagation
from telethon.tl.types import Document

from .. import loader, utils


class MusicDLLib(loader.Library):
    developer = "@the_codwiz"
    version = (1, 0, 0)

    def __init__(self):
        self.config = loader.LibraryConfig(
            loader.ConfigValue(
                "timeout",
                40,
                "Timeout for downloading",
                validator=loader.validators.Integer(minimum=5),
            ),
            loader.ConfigValue(
                "retries",
                3,
                "Number of retries for downloading",
                validator=loader.validators.Integer(minimum=0),
            ),
            loader.ConfigValue(
                "lossless_priority",
                False,
                "If True, lossless music will be downloaded first",
                validator=loader.validators.Boolean(),
            ),
        )

    async def _dl(self, bot: str, full_name: str):
        try:
            return (await self._client.inline_query(bot, full_name))[0].document
        except Exception:
            return None

    async def _legacy(self, full_name: str):
        document = await self._dl("@vkm4bot", full_name)
        document = (
            await self._dl("@spotifysavebot", full_name) if not document else document
        )
        document = await self._dl("@lybot", full_name) if not document else document
        return document

    async def dl(
        self,
        full_name: str,
        only_document: bool = False,
        retries: int = 0,
    ) -> typing.Union[Document, str]:
        try:
            if not self.config["lossless_priority"]:
                document = await self._legacy(full_name)

            if self.config["lossless_priority"] or not document:
                try:
                    q = await self._client.inline_query("@losslessrobot", full_name)
                except BotResponseTimeoutError:
                    if retries >= self.config["retries"]:
                        raise Exception("Failed to download")

                    await asyncio.sleep(3)
                    return await self.dl(full_name, only_document, retries + 1)

                result = q.result.results[0]
                if not getattr(
                    getattr(result, "send_message", None), "reply_markup", None
                ):
                    document = result.document
                    if text := getattr(
                        getattr(result, "send_message", None), "message", None
                    ):
                        if "FLAC" in text:
                            document.is_flac = True
                else:
                    m = await q[0].click("me")

                    dl_event = asyncio.Event()
                    document = None

                    @self._client.on(MessageEdited(chats=utils.get_chat_id(m)))
                    async def handler(event: MessageEdited):
                        nonlocal document
                        try:
                            if (
                                event.message.id == m.id
                                and (
                                    not getattr(event.message, "reply_markup", None)
                                    or all(
                                        button.text
                                        != "Подождите, трек скоро скачается."
                                        for button in utils.array_sum(
                                            [
                                                row.buttons
                                                for row in event.message.reply_markup.rows
                                            ]
                                        )
                                    )
                                )
                                and event.message.document
                            ):
                                document = event.message.document
                                if text := getattr(event.message, "message", None):
                                    if "FLAC" in text:
                                        document.is_flac = True
                                dl_event.set()

                                raise StopPropagation
                        except StopPropagation:
                            raise
                        except Exception:
                            logging.exception("Failed to download")

                    try:
                        await asyncio.wait_for(
                            dl_event.wait(),
                            timeout=self.config["timeout"],
                        )
                    except Exception:
                        await m.delete()
                        document = None
                    else:
                        await m.delete()
        except Exception:
            logging.debug("Can't download", exc_info=True)
            document = None

        if not document:
            document = await self._legacy(full_name)

        if not document:
            return None

        if only_document:
            return document

        file = io.BytesIO(await self._client.download_file(document, bytes))
        file.name = "audio.mp3"

        try:
            skynet = await utils.run_sync(
                requests.post,
                "https://siasky.net/skynet/skyfile",
                files={"file": file},
            )
        except ConnectionError:
            return None

        return f"https://siasky.net/{skynet.json()['skylink']}"