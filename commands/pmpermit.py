# -----------------------------------------------------------
# Astra-Userbot - WhatsApp Userbot Framework
# Copyright (c) 2026 Aman Kumar Pandey
# https://github.com/paman7647/Astra-Userbot
# Licensed under the MIT License.
# See LICENSE file in the project root for full license text.
# -----------------------------------------------------------

from config import config
from utils.state import state
from . import *

@astra_command(
    name="pmpermit",
    description="Toggle PM Protection or permit/deny users",
    category="Owner",
    aliases=[],
    usage="<on|off|approve|deny> [user_id]",
    owner_only=True
)
async def pmpermit_handler(client: Client, message: Message):
    """Toggle PM Protection or permit/deny users"""
    try:
        args_list = extract_args(message)
        
        if not args_list:
            status = "Active 🛡️" if config.ENABLE_PM_PROTECTION else "Inactive 🔓"
            return await smart_reply(message, f" *PM Protection Status:* {status}\n\nUse `.pmpermit <on|off>` to toggle.")

        action = args_list[0].lower()

        if action == "on":
            config.ENABLE_PM_PROTECTION = True
            await smart_reply(message, " ✅ *PM Protection Enabled!*")
        elif action == "off":
            config.ENABLE_PM_PROTECTION = False
            await smart_reply(message, " 🔓 *PM Protection Disabled.*")
        elif action in ["approve", "permit", "a"]:
            target_id = None
            if len(args_list) > 1:
                target_id = args_list[1]
            elif message.has_quoted_msg:
                quoted = message.quoted
                target_id = quoted.author or quoted.chat_id

            if not target_id:
                return await smart_reply(message, " 📝 *Please provide a user ID or reply to a message.*")

            if not target_id.endswith('@c.us'): target_id = f"{target_id}@c.us"
            state.permit_user(target_id)
            await smart_reply(message, f" ✅ *User permitted:* {target_id}")

        elif action in ["deny", "d"]:
            target_id = None
            if len(args_list) > 1:
                target_id = args_list[1]
            elif message.has_quoted_msg:
                quoted = message.quoted
                target_id = quoted.author or quoted.chat_id

            if not target_id:
                return await smart_reply(message, " 📝 *Please provide a user ID or reply to a message.*")

            if not target_id.endswith('@c.us'): target_id = f"{target_id}@c.us"
            state.deny_user(target_id)
            await smart_reply(message, f" ❌ *User denied:* {target_id}")
        else:
            await smart_reply(message, " ❌ *Invalid action.*")
    except Exception as e:
        await smart_reply(message, f" ❌ Error: {str(e)}")
        await report_error(client, e, context='Command pmpermit failed')
