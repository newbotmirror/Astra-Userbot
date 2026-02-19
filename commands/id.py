# -----------------------------------------------------------
# Astra-Userbot - WhatsApp Userbot Framework
# Copyright (c) 2026 Aman Kumar Pandey
# https://github.com/paman7647/Astra-Userbot
# Licensed under the MIT License.
# See LICENSE file in the project root for full license text.
# -----------------------------------------------------------

"""
Identity Utility: User & Chat Information
-----------------------------------------
Retrieves unique identifiers (IDs) for chats and users.
Essential for configuring permissions and debugging.
"""

from . import *

@astra_command(
    name="id",
    description="Get the current Chat ID and User ID.",
    category="Utility",
    aliases=["info", "whois"],
    usage="[reply]",
    is_public=True
)
async def id_handler(client: Client, message: Message):
    """
    Renders a detailed info card with Chat ID, User ID, and Sender info.
    """
    try:
        chat_id = message.chat_id
        sender_id = message.sender_id
        
        target_id = sender_id
        target_name = "You"
        
        reply_msg = ""

        # Handle Reply
        if message.has_quoted_msg and message.quoted_participant:
            target_id = message.quoted_participant.user
            target_name = "Target User"
            reply_msg = f"👤 **Target ID:** `{target_id}`\n"

        info_text = (
            "🆔 **Astra Identity Info**\n\n"
            f"🏠 **Chat ID:** `{chat_id}`\n"
            f"👤 **Your ID:** `{sender_id}`\n"
            f"{reply_msg}"
        )
        
        await smart_reply(message, info_text)

    except Exception as e:
        await report_error(client, e, context='ID command failure')
