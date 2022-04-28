
import asyncio
import os

import cv2
import numpy as np
from PIL import Image, ImageDraw

from . import catub, edit_delete, edit_or_reply

plugin_category = "extra"


@catub.cat_cmd(
    pattern="rund$",
    command=("rund", plugin_category),
    info={
        "header": "Make Round Stickers.",
        "usage": [
            "{tr}rund",
        ],
    },
)
async def ultdround(event):
    ureply = await event.get_reply_message()
    xx = await edit_or_reply(event, "`Processing...`")
    if not (ureply and (ureply.media)):
        await xx.edit("`Reply to any media`")
        return
    ultt = await ureply.download_media()
    if ultt.endswith(".tgs"):
        await xx.edit("`OwO Animated Sticker... 👀`")
        cmd = ["lottie_convert.py", ultt, "ult.png"]
        file = "ult.png"
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()
        stderr.decode().strip()
        stdout.decode().strip()
    elif ultt.endswith((".gif", ".mp4", ".mkv")):
        await xx.edit("`Processing...`")
        img = cv2.VideoCapture(ultt)
        heh, lol = img.read()
        cv2.imwrite("ult.png", lol)
        file = "ult.png"
    else:
        file = ultt
    img = Image.open(file).convert("RGB")
    npImage = np.array(img)
    h, w = img.size
    alpha = Image.new("L", img.size, 0)
    draw = ImageDraw.Draw(alpha)
    draw.pieslice([0, 0, h, w], 0, 360, fill=255)
    npAlpha = np.array(alpha)
    npImage = np.dstack((npImage, npAlpha))
    Image.fromarray(npImage).save("ult.webp")
    await event.client.send_file(
        event.chat_id,
        "ult.webp",
        force_document=False,
        reply_to=event.reply_to_msg_id,
    )
    await xx.delete()
    os.remove(file)
    os.remove("ult.webp")


@catub.cat_cmd(
    pattern="tgs ?(.*)",
    command=("tgs", plugin_category),
    info={
        "header": "Destory a sticker",
        "usage": "{tr}tgs <reply to a animated sticker>",
    },
)
async def tgscmd(message):
    """Tgs Killer"""
    reply = await message.get_reply_message()
    if not reply:
        await edit_delete(message, "`Reply to an animated sticker`", 3)
        return
    if not reply.file.name.endswith(".tgs"):
        await edit_delete(message, "`Reply to an animated sticker only.`", 3)
        return
    await reply.download_media("pepe.tgs")
    await edit_or_reply(message, "`Fixing this sticker...`")
    os.system("lottie_convert.py pepe.tgs json.json")
    json = open("json.json", "r")
    jsn = json.read()
    json.close()
    jsn = (
        jsn.replace("[100]", "[200]")
        .replace("[10]", "[40]")
        .replace("[-1]", "[-10]")
        .replace("[0]", "[15]")
        .replace("[1]", "[20]")
        .replace("[2]", "[17]")
        .replace("[3]", "[40]")
        .replace("[4]", "[37]")
        .replace("[5]", "[60]")
        .replace("[6]", "[70]")
        .replace("[7]", "[40]")
        .replace("[8]", "[37]")
        .replace("[9]", "[110]")
    )

    open("json.json", "w").write(jsn)
    os.system("lottie_convert.py json.json pepe.tgs")
    await message.reply(file="pepe.tgs")
    os.remove("json.json")
    os.remove("pepe.tgs")
    await message.delete()
