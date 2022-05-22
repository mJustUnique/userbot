# By - LΣGΣΠD | @Hey_LEGEND
# From Kangers Import Madafaka
# Keep Credits Madafaka !!

import asyncio
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
async def decide(event):
    "Will Decide For You."
    if event.fwd_from:
        return
    legend = event.pattern_match.group(1)
    await reply_id(event)
    if not legend:
        return await edit_delete(event, "What Should I Decide? Gib Value Kid !!", 15)
    options = legend.split()
    comma = ", "
    await edit_delete(event, f"**From Options :** __{comma.join(options)}__\n\n**Randomly Choosen :** __{random.choice(options)}__", 120)
    
    
@catub.cat_cmd(
    pattern="(coin|flipacoin)$",
    command=("coin", plugin_category),
    info={
        "header": "Flips A Coin. (Toss)",
        "usage": [
            "{tr}coin",
            "{tr}flipacoin",
        ],
    },
)
async def coin(event):
    "Heads Tails"
    legend = ["You Got", "It's", "It Landed On", "Oh"]
    legendop = ["Heads", "Tails"]
    await event.edit("`Flipping...`")
    await asyncio.sleep(1)
    await event.edit("`Coin Is In The Air...`")
    await asyncio.sleep(1)
    await event.edit("`Falling Down !!`")
    await asyncio.sleep(1)
    await edit_delete(event, f"`Flipped A Coin And...`\n\n`{random.choice(legend)}` **{random.choice(legendop)} !!**", 120)
