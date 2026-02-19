# -----------------------------------------------------------
# Astra-Userbot - WhatsApp Userbot Framework
# Copyright (c) 2026 Aman Kumar Pandey
# https://github.com/paman7647/Astra-Userbot
# Licensed under the MIT License.
# See LICENSE file in the project root for full license text.
# -----------------------------------------------------------

"""
YouTube Media Integration
-------------------------
A high-performance media downloading plugin that utilizes a Node.js 
bridge to execute yt-dlp operations safely outside the Python event loop.
"""

import os
import time
import shutil
import asyncio
import json
from . import *
from config import config

@astra_command(
    name="youtube",
    description="Download media from YouTube (Audio or Video).",
    category="Media",
    aliases=["yt", "ytdl"],
    usage="<url> [video|audio] [--doc]",
    owner_only=False
)
async def youtube_handler(client: Client, message: Message):
    """
    Handles media download requests. 
    Routes the URL to the JavaScript bridge for secure processing.
    """
    try:
        args_list = extract_args(message)
        if not args_list:
            return await smart_reply(message, " ❌ Please provider a valid YouTube URL.")

        # System validation
        if not shutil.which("yt-dlp"):
             return await smart_reply(message, "⚠️ `yt-dlp` system dependency is missing. Please run `setup.sh`.")

        node_bin = shutil.which("node")
        if not node_bin:
            return await smart_reply(message, "⚠️ `Node.js` is required for this operation.")

        # Argument parsing
        url = args_list[0]
        as_doc = any(opt in args_list for opt in ["doc", "document", "--doc", "--document"])
        mode = "video" if "video" in [arg.lower() for arg in args_list] else "audio"

        status_msg = await smart_reply(message, f" ⏳ *Astra Media Engine processing {mode}...*")

        # Workspace preparation
        temp_dir = os.path.join(os.getcwd(), "temp")
        os.makedirs(temp_dir, exist_ok=True)

        # Cross-language Bridge Execution
        # -------------------------------
        # We invoke the Node.js bridge to handle complex yt-dlp logic, 
        # which provides better bypasses and concurrency for media downloads.
        bridge_script = os.path.join(os.path.dirname(os.path.dirname(__file__)), "utils", "js_downloader.js")
        
        cookies_file = getattr(config, 'YOUTUBE_COOKIES_FILE', '') or ''
        cookies_browser = getattr(config, 'YOUTUBE_COOKIES_FROM_BROWSER', '') or ''

        process = await asyncio.create_subprocess_exec(
            node_bin, bridge_script,
            url, mode, 
            cookies_file, cookies_browser,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout_raw, stderr_raw = await process.communicate()

        if process.returncode != 0:
            err_log = stderr_raw.decode(errors='ignore')[:800]
            await status_msg.edit(f" ❌ Media Core Error:\n```{err_log}```")
            return

        # Result retrieval
        try:
            res = json.loads(stdout_raw.decode())
            if not res.get('success'):
                raise Exception(res.get('error', 'Bridge synchronization failure'))
            files = res.get('files', [])
        except Exception as jerr:
            return await status_msg.edit(f" ❌ Bridge communication error: {str(jerr)}")

        if not files:
            return await status_msg.edit(" ❌ Target file not found post-download.")

        file_path = files[0]

        # Safety & Governance
        try:
            size_mb = os.path.getsize(file_path) / (1024*1024)
            if size_mb > config.MAX_FILE_SIZE_MB:
                os.remove(file_path) # Cleanup immediately
                return await status_msg.edit(f"❌ File exceeds governance limit ({size_mb:.1f}MB > {config.MAX_FILE_SIZE_MB}MB).")
        except Exception:
            pass

        # Content Delivery
        await status_msg.edit(f" 📤 *Delivering {mode}{' as document' if as_doc else ''}...*")
        try:
            if mode == "audio":
                await client.send_audio(message.chat_id, file_path, reply_to=message.id)
            else:
                await client.send_video(message.chat_id, file_path, reply_to=message.id)
            await status_msg.delete()
        except Exception as upload_err:
            # Fallback to general file send if typed send fails
            try:
                await client.send_file(message.chat_id, file_path, document=True, reply_to_message_id=message.id)
                await status_msg.delete()
            except Exception as final_err:
                await status_msg.edit(f" ❌ Delivery failed: {str(final_err)}")
                await report_error(client, final_err, context=f'YouTube delivery failed: {url}')

        # Workspace Cleanup
        finally:
            if os.path.exists(file_path):
                try: os.remove(file_path)
                except: pass

    except Exception as e:
        await smart_reply(message, f" ❌ System Error: {str(e)}")
        await report_error(client, e, context='YouTube command root failure')
