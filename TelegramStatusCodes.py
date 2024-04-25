# ---------------------------------------------------------------------------------
# Name: TelegramStatusCodes
# Description: Dictionary of telegram status codes
# Author: @hikka_mods
# ---------------------------------------------------------------------------------

# 🔒    Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# meta developer: @hikka_mods
# scope: Api TelegramStatusCodes
# scope: Api TelegramStatusCodes 0.0.1
# ---------------------------------------------------------------------------------

from telethon.tl.types import Message

from .. import loader, utils

__version__ = (1, 0, 0)

responses = {
    300: (
        "⛔ SEE_OTHER",
        "The request must be repeated, but directed to a different data center.",
    ),
    400: (
        "⛔ BAD_REQUEST",
        "The query contains errors. In the event that a request was created using a form and contains user generated data, the user should be notified that the data must be corrected before the query is repeated.",
    ),
    401: (
        "⛔ UNAUTHORIZED",
        "There was an unauthorized attempt to use functionality available only to authorized users.",
    ),
    403: (
        "⛔ FORBIDDEN",
        "Privacy violation. For example, an attempt to write a message to someone who has blacklisted the current user.",
    ),
    404: (
        "⛔ NOT_FOUND",
        "An attempt to invoke a non-existent object, such as a method",
    ),
    406: (
        "⛔ NOT_ACCEPTABLE",
        """
Similar to <b>400 BAD_REQUESTS</b>, but the app must display the error to the user a bit differently.
Do not display any visible error to the user when receiving the <b>rpc_error</b> constructor: instead, wait for an <a href="https://core.telegram.org/constructor/updateServiceNotification ">updateServiceNotification</a> update, and handle it as usual.
Basically, an <a href="https://core.telegram.org/constructor/updateServiceNotification"updateServiceNotification</a> <b>pop-up</b> update will be emitted independently (ie NOT as an <a href="https://core.telegram.org/type/Updates">Updates</a> constructor inside <b>rpc_result</b> but as a normal update) immediately after emission of a 406 <b>rpc_error</b>: the update will contain the actual localized error message to show to the user with a UI popup.

An exception to this is the <b>AUTH_KEY_DUPLICATED</b> error, which is only emitted if any of the non-media DC detects that an authorized session is sending requests in parallel from two separate TCP connections, from the same or different IP addresses.
Note that parallel connections are still allowed and actually recommended for media DCs.
Also note that by session we mean a logged-in session identified by an <a href="https://core.telegram.org/constructor/authorization">authorization</a> constructor, fetchable using <a href="https://core.telegram.org/method/account.getAuthorizations">account.getAuthorizations</a>, not an MTProto session.

If the client receives an <b>AUTH_KEY_DUPLICATED</b> error, the session was already invalidated by the server and the user must generate a new auth key and login again.""",
    ),
    420: (
        "⛔ FLOOD",
        "The maximum allowed number of attempts to invoke the given method with the given input parameters has been exceeded. For example, in an attempt to request a large number of text messages (SMS) for the same phone number.",
    ),
    500: (
        "⛔ INTERNAL",
        """An internal server error occurred while a request was being processed; for example, there was a disruption while accessing a database or file storage.

If a client receives a 500 error, or you believe this error should not have occurred, please collect as much information as possible about the query and error and send it to the developers""",
    ),
}


@loader.tds
class TelegramStatusCodes(loader.Module):
    """Dictionary of telegram status codes"""

    strings = {
        "name": "TelegramStatusCodes",
        "args_incorrect": "<b>Incorrect args</b>",
        "not_found": "<b>Code not found</b>",
        "syntax_error": "<b>Args are mandatory</b>",
        "scode": "<b>{} {}</b>\n⚜️ Code Description: <i>{}</i>",
    }

    strings_ru = {
        "args_incorrect": "<b>Неверные аргументы</b>",
        "not_found": "<b>Код не найден</b>",
        "syntax_error": "<b>Аргументы обязательны</b>",
        "_cmd_doc_httpsc": "<код> - Получить информацию о Telegram error",
        "_cmd_doc_httpscs": "Показать все доступные коды",
        "_cls_doc": "Словарь telegram error",
    }

    @loader.unrestricted
    async def tgccmd(self, message: Message):
        """<statuscode> - Get status code info"""
        args = utils.get_args(message)
        if not args:
            await utils.answer(message, self.strings("syntax_error", message))

        try:
            if int(args[0]) not in responses:
                await utils.answer(message, self.strings("not_found", message))
        except ValueError:
            await utils.answer(message, self.strings("args_incorrect", message))

        await utils.answer(
            message,
            self.strings("scode", message).format(
                responses[int(args[0])][0], args[0], responses[int(args[0])][1]
            ),
        )

    @loader.unrestricted
    async def tgcscmd(self, message: Message):
        """Get all telegram status codes"""
        await utils.answer(
            message,
            "\n".join(
                [f"<b>{str(sc)}: {text}</b>" for sc, (text, _) in responses.items()]
            ),
        )
