# -----------------------------------------------------------
# Astra-Userbot - WhatsApp Userbot Framework
# Copyright (c) 2026 Aman Kumar Pandey
# https://github.com/paman7647/Astra-Userbot
# Licensed under the MIT License.
# See LICENSE file in the project root for full license text.
# -----------------------------------------------------------

"""
System Vitality Plugin
----------------------
Handles the .alive diagnostic command to verify bot connectivity 
and display current system information/versioning.
"""

from . import *
from config import config

@astra_command(
    name="alive",
    description="Check the bot's current status and system information.",
    category="General",
    aliases=[],
    usage="",
    owner_only=True
)
async def alive_handler(client: Client, message: Message):
    """
    Renders a status report containing versioning, branding, 
    and configuration metadata.
    """
    try:
        from utils.state import state
        curr_prefix = state.get_prefix()
        
        # Determine owner name dynamically
        owner_name = config.OWNER_NAME
        try:
            me = await client.get_me()
            if me and me.name:
                owner_name = me.name
        except Exception:
            pass

        # Professional formatting with Markdown
        alive_text = (
            f"✨ **Astra Userbot Connectivity Report**\n\n"
            f"*Version:* `{config.VERSION}`\n"
            f"*Build:* `dev-beta` (Stable)\n"
            f"*Active Prefix:* `{curr_prefix}`\n"
            f"*Bot User:* `{owner_name}`\n"
            f"*Owner Reference:* {config.OWNER_ID}\n\n"
            f"🚀 System is operational. Type `{curr_prefix}help` for options."
        )
    
        await smart_reply(message, alive_text)
        
    except Exception as e:
        # Diagnostic fallback
        logger = getattr(client, 'logger', None)
        if logger:
            logger.error(f"Alive status check failed: {e}")
        await smart_reply(message, f" ❌ Diagnostic check failed: {str(e)}")
        await report_error(client, e, context='Command .alive execution failure')
