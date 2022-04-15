import asyncio

from telethon.errors import FloodWaitError, MessageNotModifiedError
from telethon.events import CallbackQuery

from ..Config import Config
from ..sql_helper.globals import gvarstatus


def check_owner(func):
    async def wrapper(c_q: CallbackQuery):
        if c_q.query.user_id and (
            c_q.query.user_id == Config.OWNER_ID
            or c_q.query.user_id in Config.SUDO_USERS
        ):
            try:
                await func(c_q)
            except FloodWaitError as e:
                await asyncio.sleep(e.seconds + 5)
            except MessageNotModifiedError:
                pass
        else:
            HELP_TEXT = (
                gvarstatus("HELP_TEXT")
                or "𝗦𝘁𝗼𝗽...✋ 𝐎𝐧𝐥𝐲 𝐌𝐲 𝐁𝐨𝐬𝐬 𝐂𝐚𝐧 𝐀𝐜𝐜𝐞𝐬𝐬 𝐓𝐡𝐢𝐬 - 𝐍𝐨𝐭 𝐅𝐨𝐫 𝐘𝐨𝐮 𝐁𝐢𝐭𝐜𝐡...!"
            )
            await c_q.answer(
                HELP_TEXT,
                alert=True,
            )

    return wrapper
