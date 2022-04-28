# LΣGΣΠD | @Hey_LEGEND

import random
from userbot import catub
from ..core.managers import edit_delete
from ..helpers.utils import reply_id

plugin_category = "utils"


@catub.cat_cmd(
    pattern="decide ?(.*)",
    command=("decide", plugin_category),
    info={
        "header": "Chooses a random values in the given options, give values saparated by space.",
        "usage": [
            "{tr}decide <options>",
            "{tr}decide a b c d",
            "{tr}decide math chemistry physics biology",
        ],
    },
)
async def Gay(event):
    "Will Decide For You."
    if event.fwd_from:
        return
    legend = event.pattern_match.group(1)
    await reply_id(event)
    if not legend:
        return await edit_delete(event, "What Should I Decide? Gib Value Kid !!", 15)
    options = legend.split()
    await edit_delete(event, random.choice(options), 120)