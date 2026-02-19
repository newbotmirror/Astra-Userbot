# -----------------------------------------------------------
# Astra-Userbot - WhatsApp Userbot Framework
# Copyright (c) 2026 Aman Kumar Pandey
# https://github.com/paman7647/Astra-Userbot
# Licensed under the MIT License.
# See LICENSE file in the project root for full license text.
# -----------------------------------------------------------

import asyncio
from . import *

@astra_command(
    name="exec",
    description="Execute shell commands (Owner Only)",
    category="System",
    aliases=["sh", "bash"],
    usage="",
    owner_only=True
)
async def exec_handler(client: Client, message: Message):
    """Execute shell commands (Owner Only)"""
    try:
        args_list = extract_args(message)
        
        if not args_list:
            return await smart_reply(message, " ⚠️ Please provide a command.")

        command = " ".join(args_list)
        process = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()

        output = ""
        if stdout:
            output += f"*Output:*\n```\n{stdout.decode().strip()}\n```\n"
        if stderr:
            output += f"*Stderr:*\n```\n{stderr.decode().strip()}\n```"
    
        if not output:
            output = " ✅ Command executed (no output)."
    
        await smart_reply(message, output)
    except Exception as e:
        await smart_reply(message, f" ❌ Error: {str(e)}")
        await report_error(client, e, context='Command exec failed')
