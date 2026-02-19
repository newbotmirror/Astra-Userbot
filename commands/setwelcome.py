# -----------------------------------------------------------
# Astra-Userbot - WhatsApp Userbot Framework
# Copyright (c) 2026 Aman Kumar Pandey
# https://github.com/paman7647/Astra-Userbot
# Licensed under the MIT License.
# See LICENSE file in the project root for full license text.
# -----------------------------------------------------------

"""
Group Welcome Management
-----------------------
Allows group administrators to configure automated welcome messages 
for new participants.
"""

from utils.state import state
from . import *

@astra_command(
    name="setwelcome",
    description="Configure the automated welcome greeting for this group.",
    category="Group Management",
    aliases=["welcome"],
    usage="<greeting_text>"
)
async def setwelcome_handler(client: Client, message: Message):
    """
    Persists a custom welcome string for the current group context.
    """
    try:
        # Context Validation
        if not message.chat_id.endswith('@g.us'):
            return await smart_reply(message, " ❌ This administrative tool is restricted to group chats.")

        args_list = extract_args(message)
        welcome_text = " ".join(args_list)
        
        if not welcome_text:
            return await smart_reply(message, " 📋 Usage: `.setwelcome Welcome to {group_name}!`")

        # State Persistence
        gid = message.chat_id
        group_configs = state.state.get("group_configs", {})
        
        if gid not in group_configs:
            group_configs[gid] = {}
            
        group_configs[gid]["welcome"] = welcome_text
        state.state["group_configs"] = group_configs
        
        await asyncio.to_thread(state.save)

        await smart_reply(message, " ✅ **Welcome Registry Updated.** New participants will now receive this message.")
        
    except Exception as e:
        await smart_reply(message, f" ❌ Configuration failure: {str(e)}")
        await report_error(client, e, context='setwelcome command failed')

import asyncio # Needed for state.save threading
