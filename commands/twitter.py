# -----------------------------------------------------------
# Astra-Userbot - WhatsApp Userbot Framework
# Copyright (c) 2026 Aman Kumar Pandey
# https://github.com/paman7647/Astra-Userbot
# Licensed under the MIT License.
# See LICENSE file in the project root for full license text.
# -----------------------------------------------------------

import asyncio
import os
import time
import json
import shutil
from config import config
from . import *

@astra_command(
    name="twitter",
    description="Download Twitter video",
    category="Media",
    aliases=["tw", "x"],
    usage="<url>",
    owner_only=False
)
async def twitter_handler(client: Client, message: Message):
    """Download Twitter video"""
    try:
        args_list = extract_args(message)
        
        if not args_list:
            return await smart_reply(message, " ❌ Please provide a Twitter/X URL.")

        url = args_list[0]
        status_msg = await smart_reply(message, " ⏳ *Processing Twitter video...*")

        temp_dir = os.path.join(os.getcwd(), "temp")
        os.makedirs(temp_dir, exist_ok=True)

        timestamp = int(time.time())
        # output_tmpl = os.path.join(temp_dir, f"tw_{timestamp}_%(id)s.%(ext)s")
        
        # Use Node.js bridge to bypass Python 3.14 environment issues
        node_bin = "/opt/homebrew/bin/node"
        bridge_script = os.path.join(os.path.dirname(os.path.dirname(__file__)), "utils", "js_downloader.js")

        cookies_file = getattr(config, 'YOUTUBE_COOKIES_FILE', '') or ''
        cookies_browser = getattr(config, 'YOUTUBE_COOKIES_FROM_BROWSER', '') or ''

        bridge_cmd = [
            node_bin, bridge_script,
            url, "video", 
            cookies_file, cookies_browser
        ]
        process = await asyncio.create_subprocess_exec(
            *bridge_cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout_data, stderr_data = await process.communicate()

        if process.returncode != 0:
            err_text = stderr_data.decode(errors='ignore')[:300]
            return await status_msg.edit(f"❌ Twitter download failed via JS Bridge:\n```{err_text}```")

        try:
            res = json.loads(stdout_data.decode())
            if not res.get('success'):
                raise Exception(res.get('error', 'Unknown bridge error'))
            files_found = res.get('files', [])
        except Exception as jerr:
            return await status_msg.edit(f" ❌ Bridge output error: {str(jerr)}")

        if not files_found:
            return await status_msg.edit(" ❌ Video not found or incompatible.")

        file_path = files_found[0]
        await status_msg.edit(" 📤 *Uploading...*")

        await client.send_video(message.chat_id, file_path, caption="🐦 *Delivered from X*")
        await status_msg.delete()

        if os.path.exists(file_path): os.remove(file_path)
    except Exception as e:
        await smart_reply(message, f" ❌ Error: {str(e)}")
        await report_error(client, e, context='Command twitter failed')
