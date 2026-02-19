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
from config import config
from . import *

@astra_command(
    name="pinterest",
    description="Download Pinterest media",
    category="Media",
    aliases=["pin"],
    usage="<url>",
    owner_only=False
)
async def pinterest_handler(client: Client, message: Message):
    """Download Pinterest media"""
    try:
        args_list = extract_args(message)
        
        if not args_list:
            return await smart_reply(message, " ❌ Please provide a Pinterest URL.")

        url = args_list[0]
        status_msg = await smart_reply(message, " ⏳ *Processing Pin...*")

        temp_dir = os.path.join(os.getcwd(), "temp")
        os.makedirs(temp_dir, exist_ok=True)

        timestamp = int(time.time())
        # output_tmpl = os.path.join(temp_dir, f"pin_{timestamp}_%(id)s.%(ext)s") # Unused var

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
            return await status_msg.edit(f"❌ Pinterest download failed via JS Bridge:\n```{err_text}```")

        try:
            res = json.loads(stdout_data.decode())
            if not res.get('success'):
                raise Exception(res.get('error', 'Unknown bridge error'))
            files_found = res.get('files', [])
        except Exception as jerr:
            return await status_msg.edit(f" ❌ Bridge output error: {str(jerr)}")

        if not files_found:
            return await status_msg.edit(" ❌ Link invalid or media not found.")

        file_path = files_found[0]
        await status_msg.edit(" 📤 *Uploading...*")

        await client.send_file(message.chat_id, file_path, caption="📌 *Pinterest Media*")
        await status_msg.delete()

        if os.path.exists(file_path): os.remove(file_path)
    except Exception as e:
        await smart_reply(message, f" ❌ Error: {str(e)}")
        await report_error(client, e, context='Command pinterest failed')
