# -----------------------------------------------------------
# Astra-Userbot - WhatsApp Userbot Framework
# Copyright (c) 2026 Aman Kumar Pandey
# https://github.com/paman7647/Astra-Userbot
# Licensed under the MIT License.
# See LICENSE file in the project root for full license text.
# -----------------------------------------------------------

from . import *

@astra_command(
    name="help",
    aliases=["h", "menu"],
    description="List all commands or get help for a specific one.",
    category="Utility",
    usage="[command]",
    is_public=True
)
async def help_handler(client: Client, message: Message):
    """
    Renders an interactive help menu by parsing the global COMMANDS_METADATA registry.
    """
    import logging
    logger = logging.getLogger("Astra.Help")
    try:
        # Debug: Check metadata
        logger.info(f"Help triggered. Metadata size: {len(COMMANDS_METADATA)}")
        
        args = getattr(message, 'command', None)
        if args and not isinstance(args, str) and hasattr(args, 'args'):
            args_list = args.args
        else:
            # Fallback: Parse body manually if filter didn't attach command info or it's just a string
            body = getattr(message, 'body', "") or ""
            parts = body.split()
            args_list = parts[1:] if len(parts) > 1 else []
        
        from utils.state import state
        curr_prefix = state.get_prefix()

        if args_list:
            cmd_name = args_list[0].lower()
            # Find command in metadata
            cmd = next((c for c in COMMANDS_METADATA if c['name'] == cmd_name or cmd_name in c['aliases']), None)
            
            if not cmd:
                try:
                    return await message.edit(f"Command `{cmd_name}` not found.")
                except Exception:
                    return await message.reply(f"Command `{cmd_name}` not found.")
            
            help_text = f"📖 *Help:* `{curr_prefix}{cmd['name']}`\n"
            help_text += f"*Description:* {cmd['description']}\n"
            if cmd['aliases']:
                help_text += f"*Aliases:* `{curr_prefix}{f', {curr_prefix}'.join(cmd['aliases'])}`\n"
            help_text += f"*Category:* {cmd['category']}\n"
            help_text += f"*Usage:* `{curr_prefix}{cmd['name']} {cmd['usage']}`".strip()
            
            try:
                if message.from_me:
                    return await message.edit(help_text)
                else:
                    return await message.reply(help_text)
            except Exception:
                return await message.reply(help_text)

        # Main help menu
        categories = {}
        for cmd in COMMANDS_METADATA:
            cat = cmd['category']
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(cmd['name'])

        help_text = "🚀 *Astra Userbot Menu*\n\n"
        if not categories:
            help_text += "No commands found in metadata registry."
        
        for cat in sorted(categories.keys()):
            help_text += f"*{cat}*\n"
            cmd_list = [f"{curr_prefix}{c}" for c in sorted(categories[cat])]
            help_text += f"`{', '.join(cmd_list)}`\n\n"
        
        help_text += f"Use `{curr_prefix}help <cmd>` for details."
        
        try:
            if message.from_me:
                await message.edit(help_text)
            else:
                await message.reply(help_text)
        except Exception:
            await message.reply(help_text)

    except Exception as e:
        logger.error(f"Help command failed: {e}", exc_info=True)
        try:
            await message.edit(f"❌ Help Error: {e}")
        except:
            await message.reply(f"❌ Help Error: {e}")
