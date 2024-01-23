# Name: HikkaHost
# Description: Hikkahost manager.
# Author: @hikka_mods
# ---------------------------------------------------------------------------------

# 🔒    Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# meta developer: @hikka_mods
# scope: api HikkaHost
# scope: api HikkaHost 0.0.1
# ---------------------------------------------------------------------------------

import aiohttp
import asyncio
import json
from datetime import datetime, timedelta, timezone
from .. import loader, utils


async def _request(
    path: str,
    token: str,
    method: str = "GET"
) -> dict:
    url = 'http://api.hikkahost.tech:7777' + path
    async with aiohttp.ClientSession(trust_env=True) as session:
        async with session.request(
            method,
            url,
            headers={
                "Content-Type": "application/json",
                "token": token,
            },
            ssl=False,
        ) as response:
            return await response.json()


async def _stats(user_id, token):
    url = f"/api/host/{user_id}/stats"
    return await _request(url, token)

async def _host(user_id, token):
    url = f"/api/host/{user_id}"
    return await _request(url, token)


async def _status(user_id, token):
    url = f"/api/host/{user_id}/status"
    return await _request(url, token)

async def _logs(user_id, token):
    url = f"/api/host/{user_id}/logs/all"
    headers = {"accept": "application/json", "token": token}
    return await _request(url, token)


async def _action(user_id, token):
    url = f"/api/host/{user_id}?action=restart"
    return await _request(url, token, 'PUT')


def bytes_to_megabytes(b: int):
    return round(b / 1024 / 1024, 1)


@loader.tds
class HikkahostMod(loader.Module):
    """Hikkahost manager."""

    strings = {
        "name": "HikkaHost",
        "info": (
            "<emoji document_id=5879770735999717115>👤</emoji> <b>Панель информации</b>\n\n"
            "<emoji document_id=5974526806995242353>🆔</emoji> <b>Server ID:</b> <code>{server_id}</code>\n"
            "<emoji document_id=6005570495603282482>🔑</emoji> <b>ID:</b> <code>{id}</code>\n"
            "<emoji document_id=5874986954180791957>📶</emoji> <b>Статус:</b> <code>{status}</code>\n"
            "<emoji document_id=5451646226975955576>⌛️</emoji> <b>Подписка закончится:</b> <code>{end_dates}</code> | <code>{days_end} дней</code>\n\n"
            "<emoji document_id=5877260593903177342>⚙️</emoji> <b>CPU:</b> <code>{cpu_percent} %</code>\n"
            "<emoji document_id=5379652232813750191>💾</emoji> <b>RAM:</b> <code>{memory} MB</code>"
        ),
        "logs": (
            "<emoji document_id=5188377234380954537>🌘</emoji> <b>Вот ваши логи</b>"
        ),
        "restart": (
            "<emoji document_id=5789886476472815477>✅</emoji> <b>Запрос на рестарт отправил</b>\n"
            "Это сообщение не изменяется после рестарта"
        ),
        "loading_info": "<emoji document_id=5451646226975955576>⌛️</emoji> Загрузка...",
        "no_apikey": "<emoji document_id=5260342697075416641>🚫</emoji> Вы не указали Api Key",
    }

    def __init__(self):
        self.name = self.strings["name"]
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "token",
                None,
                validator=loader.validators.Hidden(),
            ),
        )

    async def hinfocmd(self, message):
        """Status HikkaHost"""
        message = await utils.answer(message, self.strings("loading_info"))
        if self.config["token"] is None:
            await utils.answer(message, self.strings("no_apikey"))
            return

        user_id = self.tg_id
        token = self.config['token']
        data = await _stats(user_id, token)
        datas = await _status(user_id, token)

        memory_stats = data["stats"]["memory_stats"]["usage"]
        memory = bytes_to_megabytes(memory_stats)
        limit = data["stats"]["pids_stats"]["limit"]
        cpu_stats_usage = data["stats"]["cpu_stats"]["cpu_usage"]["total_usage"]
        system_cpu_usage = data["stats"]["cpu_stats"]["system_cpu_usage"]

        host = await _host(user_id, token)
        server_id = host["host"]["server_id"]
        target_data = datetime.fromisoformat(host["host"]["end_date"].replace("Z", "+00:00")).replace(tzinfo=timezone.utc)
        current_data = datetime.now(timezone.utc)
        days_end = (target_data - current_data).days
        data_end = current_data.strftime("%d-%m-%Y %H-%M")
        end_dates = (current_data + timedelta(days=days_end)).strftime("%d-%m-%Y")

        if cpu_stats_usage and system_cpu_usage:
            cpu_percent = round((cpu_stats_usage / system_cpu_usage) * 100.0, 2)

        if "status" in datas and datas["status"] == "running":
            status = "работает"

        await utils.answer(
            message,
            self.strings("info").format(
                server_id=server_id, id=user_id, status=status, end_dates=end_dates, days_end=days_end,  cpu_percent=cpu_percent, memory=memory
            ),
        )

    async def hlogscmd(self, message):
        """Logs HikkaHost"""

        if self.config["token"] is None:
            await utils.answer(message, self.strings("no_apikey"))
            return

        user_id = self.tg_id
        token = self.config['token']
        data = await _logs(user_id, token)

        files_log = data["logs"]

        with open("log.txt", "w") as log_file:
            json.dump(files_log, log_file)

        await utils.answer_file(message, "log.txt", self.strings("logs"))

    async def hrestartcmd(self, message):
        """Restart HikkaHost"""
        await utils.answer(message, self.strings("restart"))

        if self.config["token"] is None:
            await utils.answer(message, self.strings("no_apikey"))
            return

        user_id = self.tg_id
        token = self.config['token']

        data = await _action(user_id, token)
