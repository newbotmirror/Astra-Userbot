# -----------------------------------------------------------
# Astra-Userbot - WhatsApp Userbot Framework
# Copyright (c) 2026 Aman Kumar Pandey
# https://github.com/paman7647/Astra-Userbot
# Licensed under the MIT License.
# See LICENSE file in the project root for full license text.
# -----------------------------------------------------------

"""
Fun Utility: Fake Hack
----------------------
Simulates a hacking sequence for entertainment purposes.
WARNING: This is purely visual and does not actually hack anything.
"""

import asyncio
import random
from . import *

@astra_command(
    name="hack",
    description="Simulate a hacking attack on a user or chat.",
    category="Fun",
    aliases=["hacker"],
    usage="<target>",
    is_public=True
)
async def hack_handler(client: Client, message: Message):
    """
    Plays an animated sequence of "hacking" steps.
    """
    try:
        args_list = extract_args(message)
        target = "Target System"
        
        if args_list:
            target = " ".join(args_list)
        elif message.has_quoted_msg:
            if message.quoted_participant:
                target = f"@{message.quoted_participant.user}"
            else:
                target = "Current Chat"

        status_msg = await smart_reply(message, f" 💻 *Initiating Hack on {target}...*")
        
        steps = [
            " 🔍 *Scanning for vulnerabilities...*",
            " 🔓 *Bypassing firewall...*",
            " 🔑 *Brute-forcing PIN...* `1234` ❌",
            " 🔑 *Brute-forcing PIN...* `9999` ❌",
            " 🔑 *Brute-forcing PIN...* `0000` ✅ *Access Granted!*",
            " 📂 *Downloading Chat History...* `[20%]`",
            " 📂 *Downloading Chat History...* `[56%]`",
            " 📂 *Downloading Chat History...* `[100%]`",
            " 📸 *Stealing Gallery Photos...*",
            " 🤐 *Exporting Private Keys...*",
            " ☁️ *Uploading to Dark Web...*",
            f" ✅ **HACK COMPLETE!**\n\n_Target {target} has been compromised._"
        ]

        for step in steps:
            await asyncio.sleep(1.5)
            await status_msg.edit(step)

    except Exception as e:
        await report_error(client, e, context='Hack command failure')
