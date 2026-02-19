# -----------------------------------------------------------
# Astra-Userbot - WhatsApp Userbot Framework
# Copyright (c) 2026 Aman Kumar Pandey
# https://github.com/paman7647/Astra-Userbot
# Licensed under the MIT License.
# See LICENSE file in the project root for full license text.
# -----------------------------------------------------------

import random
import aiohttp
import base64
from . import *

@astra_command(
    name="meme",
    description="Get a random meme from Reddit",
    category="Fun",
    aliases=[],
    usage="",
    owner_only=False
)
async def meme_handler(client: Client, message: Message):
    """Get a random meme from Reddit"""
    try:
        import asyncio
        _ = extract_args(message)
        
        status_msg = await smart_reply(message, " 🇮🇳 *Fetching a spicy meme...*")
        
        # Expanded list for better variety
        subreddits = [
            'IndianDankMemes', 'indiameme', 'indiamemer', 'DesiMeme', 
            'bakchodi', 'bollywoodmemes', 'IndianMeyMeys', 'SaimanSays',
            'dankmemes', 'memes', 'wholesomememes', 'ProgrammerHumor', 'techhumor'
        ]
        
        found_meme = False
        last_error = None

        async with aiohttp.ClientSession() as session:
            # Retry up to 3 times
            for attempt in range(1, 4):
                try:
                    random_sub = random.choice(subreddits)
                    # Primary API
                    async with session.get(f"https://meme-api.com/gimme/{random_sub}") as resp:
                        if resp.status != 200:
                            last_error = f"API Error {resp.status}"
                            continue

                        data = await resp.json()

                        if data.get('nsfw'):
                            last_error = "NSFW content filter"
                            continue # Skip NSFW

                        url = data.get('url')
                        title = data.get('title')
                        subreddit = data.get('subreddit')

                        if not url: 
                            last_error = "No URL found"
                            continue

                        # Download image
                        async with session.get(url) as img_resp:
                            if img_resp.status != 200:
                                last_error = "Image download failed"
                                continue

                            img_data = await img_resp.read()
                            b64_data = base64.b64encode(img_data).decode('utf-8')
                            mimetype = img_resp.headers.get('Content-Type', 'image/jpeg')

                            media = {
                                "mimetype": mimetype,
                                "data": b64_data,
                                "filename": f"meme_{subreddit}.jpg"
                            }

                            await client.send_media(
                                message.chat_id, 
                                media, 
                                caption=f"*{title}*\nSubreddit: r/{subreddit}\n_Source: meme-api_",
                                quoted_message_id=message.id
                            )
                            found_meme = True
                            await status_msg.delete()
                            break # Success!

                except Exception as loop_e:
                    last_error = str(loop_e)
                    await asyncio.sleep(0.5)
            
            if not found_meme:
                await status_msg.edit(f" ❌ Failed to fetch meme after 3 attempts.\nLast error: {last_error}")

    except Exception as e:
        await smart_reply(message, f" ❌ Error: {str(e)}")
        await report_error(client, e, context='Command meme failed')

@astra_command(
    name="dmeme",
    description="Get a random NSFW/Dark meme from Reddit",
    category="Fun",
    aliases=["nsfwmeme", "darkmeme"],
    usage="",
    owner_only=False
)
async def dmeme_handler(client: Client, message: Message):
    """Get a random NSFW/Dark meme from Reddit"""
    try:
        import asyncio
        _ = extract_args(message)
        
        status_msg = await smart_reply(message, " 🔞 *Fetching a spicy NSFW meme...*")
        
        # NSFW Subreddits list
        subreddits = [
            'nsfw_memes', 'Dark_Humor', 'ImGoingToHellForThis', 
            'offensivememes', 'dankmemesnsfw', 'cursedimages',
            'IndianDankMemes', 'HolUp', 'dark_memes', 'memes_of_the_dank',
            'hentaimemes', 'animememes', 'GoodAnimemes'
        ]
        
        found_meme = False
        last_error = None

        async with aiohttp.ClientSession() as session:
            # Retry up to 5 times
            for attempt in range(1, 6):
                try:
                    random_sub = random.choice(subreddits)
                    
                    # Reddit JSON API (meme-api doesn't support NSFW well)
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                        'Accept': 'application/json'
                    }
                    
                    url = f"https://www.reddit.com/r/{random_sub}/random.json?limit=1"
                    
                    async with session.get(url, headers=headers) as resp:
                        if resp.status != 200:
                            last_error = f"RedditAPI Error {resp.status}"
                            
                            # Fallback to hot/top if random fails (some subs disable random)
                            if resp.status in [403, 404]:
                                async with session.get(f"https://www.reddit.com/r/{random_sub}/hot.json?limit=25", headers=headers) as hot_resp:
                                    if hot_resp.status == 200:
                                        hot_data = await hot_resp.json()
                                        children = hot_data.get('data', {}).get('children', [])
                                        if children:
                                            post = random.choice(children)['data']
                                            # Validate post
                                            if not post.get('over_18') and random_sub in ['nsfw_memes']:
                                                pass # Verify NSFW if needed, but we wanted NSFW anyway
                                            
                                            image_url = post.get('url_overridden_by_dest') or post.get('url')
                                            if image_url and (image_url.endswith('.jpg') or image_url.endswith('.png') or image_url.endswith('.jpeg')):
                                                # Use this post
                                                pass 
                                            else:
                                                continue
                                            
                                            # We found a candidate, let's process it below
                                            # (Refactoring logic to share code)
                                            pass
                                        else:
                                            continue
                                    else:
                                        continue
                            else:
                                continue
                        else:
                            # Random endpoint worked
                            json_data = await resp.json()
                            if isinstance(json_data, list) and len(json_data) > 0:
                                post = json_data[0]['data']['children'][0]['data']
                            elif isinstance(json_data, dict) and 'data' in json_data:
                                # Sometimes hot/top returns dict
                                children = json_data['data']['children']
                                if not children: continue
                                post = random.choice(children)['data']
                            else:
                                last_error = "Invalid JSON format"
                                continue

                    # Common Processing
                    image_url = post.get('url_overridden_by_dest') or post.get('url')
                    title = post.get('title')
                    subreddit = post.get('subreddit')

                    if not image_url or not image_url.startswith('http'): 
                        last_error = "No Image URL"
                        continue
                        
                    # Filter gallery links or videos if we can't handle them easily
                    if 'gallery' in image_url or 'v.redd.it' in image_url:
                        # Try to get media metadata? For now -> skip
                        last_error = "Gallery/Video skipped"
                        continue

                    # Download image
                    async with session.get(image_url) as img_resp:
                        if img_resp.status != 200:
                            last_error = "Image download failed"
                            continue

                        img_data = await img_resp.read()
                        
                        # Check size (max 20MB for stability)
                        if len(img_data) > 20 * 1024 * 1024:
                            last_error = "Image too large"
                            continue

                        b64_data = base64.b64encode(img_data).decode('utf-8')
                        mimetype = img_resp.headers.get('Content-Type', 'image/jpeg')
                        
                        if 'html' in mimetype or 'text' in mimetype:
                            last_error = "Not an image file"
                            continue

                        media = {
                            "mimetype": mimetype,
                            "data": b64_data,
                            "filename": f"dmeme_{subreddit}.jpg"
                        }

                        await client.send_media(
                            message.chat_id, 
                            media, 
                            caption=f"*{title}*\nSubreddit: r/{subreddit}",
                            quoted_message_id=message.id
                        )
                        found_meme = True
                        await status_msg.delete()
                        break # Success!

                except Exception as loop_e:
                    last_error = str(loop_e)
                    await asyncio.sleep(0.5)
            
            if not found_meme:
                await status_msg.edit(f" ❌ Failed to fetch NSFW meme after 5 attempts.\nLast error: {last_error}")

    except Exception as e:
        await smart_reply(message, f" ❌ Error: {str(e)}")
        await report_error(client, e, context='Command dmeme failed')
