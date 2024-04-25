# ---------------------------------------------------------------------------------
# Name: AniLibria
# Description: Searches and gives random agtme on the AniLibria database.
# Author: @hikka_mods
# ---------------------------------------------------------------------------------

# 🔒    Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# meta developer: @hikka_mods
# scope: AniLibria
# scope: AniLibria 0.0.1
# requires: anilibria.py
# ---------------------------------------------------------------------------------
from .. import loader, main
from ..inline.types import InlineQuery
from ..utils import rand
from aiogram.types import InlineQueryResultPhoto, CallbackQuery
from anilibria import AniLibriaClient
import datetime

ani_client = AniLibriaClient()
__version__ = (1, 0, 0)


@loader.tds
class AniLibriaMod(loader.Module):
    """Searches and gives random agtme on the AniLibria database."""

    strings = {
        "name": "AniLibria",
        "announce": "<b>The announcement</b>:",
        "status": "<b>Status</b>:",
        "type": "<b>Type</b>:",
        "genres": "<b>Genres</b>:",
        "favorite": "<b>Favourites &lt;3</b>:",  # &lt; == <
        "season": "<b>Season</b>:",
    }

    strings_ru = {
        "announce": "<b>Анонс</b>:",
        "status": "<b>Статус</b>:",
        "type": "<b>Тип</b>:",
        "genres": "<b>Жанры</b>:",
        "favorite": "<b>Избранное &lt;3</b>:",  # &lt; == <
        "season": "<b>Сезон</b>:",
    }

    link = "https://anilibria.tv"

    async def client_ready(self, client, db) -> None:
        self._client = client

    async def arandomcmd(self, message) -> None:
        """Возвращает случайный тайтл из базы"""
        anime_title = await ani_client.get_random_title()

        text = f"{anime_title.names.ru} \n"
        text += f"{self.strings['status']} {anime_title.status.string}\n\n"
        text += f"{self.strings['type']} {anime_title.type.full_string}\n"
        text += f"{self.strings['season']} {anime_title.season.string}\n"
        text += f"{self.strings['genres']} {' '.join(anime_title.genres)}\n\n"

        text += f"<code>{anime_title.description}</code>\n\n"
        text += f"{self.strings['favorite']} {anime_title.in_favorites}"

        kb = [
            [
                {
                    "text": "Ссылка",
                    "url": f"https://anilibria.tv/release/{anime_title.code}.html",
                }
            ]
        ]

        kb.extend(
            [
                {
                    "text": f"{torrent.quality.string}",
                    "url": f"https://anilibria.tv/{torrent.url}",
                }
            ]
            for torrent in anime_title.torrents.list
        )
        kb.append([{"text": "🔃 Обновить", "callback": self.inline__update}])
        kb.append([{"text": "🚫 Закрыть", "callback": self.inline__close}])

        await self.inline.form(
            text=text,
            photo=self.link + anime_title.posters.original.url,
            message=message,
            reply_markup=kb,
            silent=True,
        )

    async def asearch_inline_handler(self, query: InlineQuery) -> None:
        """
        Возвращает список найденных по названию тайтлов
        """
        text = query.args

        if not text:
            return

        anime_titles = await ani_client.search_titles(search=text)

        inline_query = []
        for anime_title in anime_titles:
            title_text = f"{anime_title.names.ru} | {anime_title.names.en}\n"
            title_text += f"{self.strings['status']} {anime_title.status.string}\n\n"
            title_text += f"{self.strings['type']} {anime_title.type.full_string}\n"
            title_text += f"{self.strings['season']} {anime_title.season.string} {anime_title.season.year}\n"
            title_text += f"{self.strings['genres']} {' '.join(anime_title.genres)}\n\n"

            title_text += f"<code>{anime_title.description}</code>\n\n"
            title_text += f"{self.strings['favorite']} {anime_title.in_favorites}"

            inline_query.append(
                InlineQueryResultPhoto(
                    id=str(anime_title.code),
                    title=anime_title.names.ru,
                    description=anime_title.type.full_string,
                    caption=title_text,
                    thumb_url=self.link + anime_title.posters.small.url,
                    photo_url=self.link + anime_title.posters.original.url,
                    parse_mode="html",
                )
            )
        await query.answer(inline_query, cache_time=0)

    async def inline__close(self, call: CallbackQuery) -> None:
        await call.delete()

    async def inline__update(self, call: CallbackQuery) -> None:
        anime_title = await ani_client.get_random_title()

        text = f"{anime_title.names.ru} \n"
        text += f"{self.strings['status']} {anime_title.status.string}\n\n"
        text += f"{self.strings['type']} {anime_title.type.full_string}\n"
        text += f"{self.strings['season']} {anime_title.season.string}\n"
        text += f"{self.strings['genres']} {' '.join(anime_title.genres)}\n\n"

        text += f"<code>{anime_title.description}</code>\n\n"
        text += f"{self.strings['favorite']} {anime_title.in_favorites}"

        kb = [
            [
                {
                    "text": "Ссылка",
                    "url": f"https://anilibria.tv/release/{anime_title.code}.html",
                }
            ]
        ]

        kb.extend(
            [
                {
                    "text": f"{torrent.quality.string}",
                    "url": f"https://anilibria.tv/{torrent.url}",
                }
            ]
            for torrent in anime_title.torrents.list
        )
        kb.append([{"text": "🔃 Обновить", "callback": self.inline__update}])
        kb.append([{"text": "🚫 Закрыть", "callback": self.inline__close}])

        await call.edit(
            text=text,
            photo=self.link + anime_title.posters.original.url,
            reply_markup=kb,
        )
