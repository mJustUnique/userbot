import random
import re
import time
from datetime import datetime
from platform import python_version

import requests
from telethon import version
from telethon.errors.rpcerrorlist import (
    MediaEmptyError,
    WebpageCurlFailedError,
    WebpageMediaEmptyError,
)
from telethon.events import CallbackQuery

from userbot import StartTime, catub, catversion

from ..Config import Config
from ..core.managers import edit_or_reply
from ..helpers.functions import catalive, check_data_base_heal_th, get_readable_time
from ..helpers.utils import reply_id
from ..sql_helper.globals import gvarstatus
from . import mention

plugin_category = "utils"


@catub.cat_cmd(
    pattern="alive$",
    command=("alive", plugin_category),
    info={
        "header": "To check bot's alive status",
        "options": "To show media in this cmd you need to set ALIVE_PIC with media link, get this by replying the media by .tgm",
        "usage": [
            "{tr}alive",
        ],
    },
)
async def amireallyalive(event):
    "A kind of showing bot details"
    reply_to_id = await reply_id(event)
    ANIME = None
    cat_caption = gvarstatus("ALIVE_TEMPLATE") or temp
    if "ANIME" in cat_caption:
        data = requests.get("https://animechan.vercel.app/api/random").json()
        ANIME = f"**“{data['quote']}” - {data['character']} ({data['anime']})**"
    uptime = await get_readable_time((time.time() - StartTime))
    start = datetime.now()
    catevent = await edit_or_reply(event, "`Checking...`")
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    _, check_sgnirts = check_data_base_heal_th()
    EMOJI = gvarstatus("ALIVE_EMOJI") or " ⚡ "
    ALIVE_TEXT = gvarstatus("ALIVE_TEXT") or """𝐀 𝐏𝐫𝐨𝐦𝐢𝐬𝐞 𝐌𝐞𝐚𝐧𝐬 𝐄𝐯𝐞𝐫𝐲𝐭𝐡𝐢𝐧𝐠 𝐁𝐮𝐭,
𝐎𝐧𝐜𝐞 𝐈𝐭'𝐬 𝐁𝐫𝐨𝐤𝐞𝐧, 𝐒𝐨𝐫𝐫𝐲 𝐌𝐞𝐚𝐧𝐬 𝐍𝐨𝐭𝐡𝐢𝐧𝐠."""
    CAT_IMG = gvarstatus("ALIVE_PIC") or "https://telegra.ph/file/78e33992bcd940b4e75f3.jpg"
    caption = cat_caption.format(
        ALIVE_TEXT=ALIVE_TEXT,
        ANIME=ANIME,
        EMOJI=EMOJI,
        mention=mention,
        uptime=uptime,
        telever=version.__version__,
        catver=catversion,
        pyver=python_version(),
        dbhealth=check_sgnirts,
        ping=ms,
    )
    if CAT_IMG:
        CAT = list(CAT_IMG.split())
        PIC = random.choice(CAT)
        try:
            await event.client.send_file(
                event.chat_id, PIC, caption=caption, reply_to=reply_to_id
            )
            await catevent.delete()
        except (WebpageMediaEmptyError, MediaEmptyError, WebpageCurlFailedError):
            return await edit_or_reply(
                catevent,
                f"**Media Value Error !!**\n__Change the link by __`.setdv`\n\n**__Can't get media from this link :-**__ `{PIC}`",
            )
    else:
        await edit_or_reply(
            catevent,
            caption,
        )


temp = """{ALIVE_TEXT}

**{EMOJI} Ping :** `{ping}`
**{EMOJI} Boss :** {mention}
**{EMOJI} Uptime :** `{uptime}`
**{EMOJI} Database :** `{dbhealth}...`
**{EMOJI} Bot Version :** `{catver}`
**{EMOJI} Python Version :** `{pyver}`
**{EMOJI} Telethon Version :** `{telever}`"""



@catub.cat_cmd(
    pattern="ialive$",
    command=("ialive", plugin_category),
    info={
        "header": "To check bot's alive status via inline mode",
        "options": "To show media in this cmd you need to set ALIVE_PIC with media link, get this by replying the media by .tgm",
        "usage": [
            "{tr}ialive",
        ],
    },
)
async def amireallyalive(event):
    "A kind of showing bot details by your inline bot"
    reply_to_id = await reply_id(event)
    EMOJI = gvarstatus("ALIVE_EMOJI") or " ⚡ "
    uptime = await get_readable_time((time.time() - StartTime))
    start = datetime.now()
    catevent = await edit_or_reply(event, "`Checking...`")
    await catevent.delete()
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    bot_caption = "**UserBot is Up and Running**\n\n"
    bot_caption += f"**{EMOJI} Ping :** `{ms}`\n"
    bot_caption += f"**{EMOJI} Boss :** {mention}\n"
    bot_caption += f"**{EMOJI} Uptime :** `{uptime}`\n"
    bot_caption += f"**{EMOJI} Bot Version :** `{catversion}`\n"
    bot_caption += f"**{EMOJI} Python Version :** `{python_version()}\n`"
    bot_caption += f"**{EMOJI} Telethon version :** `{version.__version__}\n`"
    results = await event.client.inline_query(Config.TG_BOT_USERNAME, bot_caption)
    await results[0].click(event.chat_id, reply_to=reply_to_id, hide_via=True)
    await event.delete()


@catub.tgbot.on(CallbackQuery(data=re.compile(b"stats")))
async def on_plug_in_callback_query_handler(event):
    statstext = await catalive(StartTime)
    await event.answer(statstext, cache_time=0, alert=True)
