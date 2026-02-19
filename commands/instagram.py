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
    name="instagram",
    description="Download Instagram post/reel",
    category="Media",
    aliases=["ig", "reel"],
    usage="<url>",
    owner_only=False
)
async def instagram_handler(client: Client, message: Message):
    """Download Instagram post/reel"""
    try:
        args_list = extract_args(message)
        
        if not args_list:
            return await smart_reply(message, " ❌ Please provide an Instagram URL.")

        url = args_list[0]
        
        # Ensure yt-dlp is available
        if not shutil.which("yt-dlp") and not shutil.which("youtube-dl"):
            return await smart_reply(message, "❌ `yt-dlp` not found on the host. Install yt-dlp or youtube-dl to use this command.")

        status_msg = await smart_reply(message, " ⏳ *Processing Instagram media...*")

        temp_dir = os.path.join(os.getcwd(), "temp")
        os.makedirs(temp_dir, exist_ok=True)

        timestamp = int(time.time())
        
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
            return await status_msg.edit(f"❌ Instagram download failed via JS Bridge:\n```{err_text}```")

        try:
            res = json.loads(stdout_data.decode())
            if not res.get('success'):
                raise Exception(res.get('error', 'Unknown bridge error'))
            files_found = res.get('files', [])
        except Exception as jerr:
            return await status_msg.edit(f" ❌ Bridge output error: {str(jerr)}")

        if not files_found:
            return await status_msg.edit(" ❌ Media not found or private account.")

        # Sort files to maintain original order (important for carousels)
        files_found.sort()

        await status_msg.edit(f" 📤 *Uploading {len(files_found)} media item(s)...*")

        for file_path in files_found:
            try:
                # send_file uses SDK's new ffprobe dimensional extraction
                await client.send_file(message.chat_id, file_path, caption="✨ *Instagram Media*")
            except Exception as send_exc:
                # fallback: send as document explicitly
                try:
                    await client.send_file(message.chat_id, file_path, caption="✨ *Instagram Media*", document=True)
                except Exception as final_exc:
                    await status_msg.edit(f" ❌ Upload failed for one or more items: {str(final_exc)}")
                    await report_error(client, final_exc, context=f'Instagram upload failed for {url}')
    
            # Cleanup individual file as we go
            if os.path.exists(file_path):
                os.remove(file_path)

        await status_msg.delete()
    except Exception as e:
        await smart_reply(message, f" ❌ Error: {str(e)}")
        await report_error(client, e, context='Command instagram failed')
