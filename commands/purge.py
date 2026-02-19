# -----------------------------------------------------------
# Astra-Userbot - WhatsApp Userbot Framework
# Copyright (c) 2026 Aman Kumar Pandey
# https://github.com/paman7647/Astra-Userbot
# Licensed under the MIT License.
# See LICENSE file in the project root for full license text.
# -----------------------------------------------------------

"""
Moderation Utility: Delete
--------------------------
Single message deletion.
"""

from . import *

@astra_command(
    name="del",
    description="Delete the replied message.",
    category="Moderation",
    aliases=["delete", "d"],
    usage="(reply)",
    owner_only=True
)
async def delete_handler(client: Client, message: Message):
    """
    .del (reply) -> deletes the replied message.
    """
    try:
        if not message.has_quoted_msg:
             return await smart_reply(message, " ⚠️ Reply to a message to delete it.")

        # Use the new shortcut in Client class
        await client.delete_message(message.chat_id.serialized, message.quoted_message_id, everyone=True)
        await message.delete()

    except Exception as e:
        # If it fails (e.g. not admin, too old), let the user know
        await smart_reply(message, f" ❌ Failed to delete: {str(e)}")
