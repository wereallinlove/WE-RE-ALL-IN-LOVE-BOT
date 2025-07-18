
import discord
from discord.ext import commands, tasks
import openai
import random
import os
from datetime import datetime
import pytz

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

openai.api_key = os.getenv("OPENAI_API_KEY")
timezone = pytz.timezone("America/New_York")

# Constants
TARGET_CHANNEL_ID = 1391828985347965019
CREATOR_ID = 112760669178241024
CREATOR_NAME = "Nick6383"

slang = ["slay", "bitch", "fr", "finesse", "opps", "flex", "deadass", "ew", "bffr", "delulu", "ate", "snatched", "gagged"]
emojis = ["💅", "🖤", "😩", "💕", "😈", "✨", "😭", "🎀", "🤭", "💔", "🔪", "👠", "💋", "😻", "🙄", "🤡"]
negative_targets = ["punkin", "patrick", "punkinloveee"]

def generate_personality_response(message):
    author = message.author.display_name
    content = message.content.lower()

    if any(name in content for name in negative_targets):
        return f"eww not {content} 😭 pls log off bitch 💅"

    if str(message.author.id) == str(CREATOR_ID):
        return f"hi bby {CREATOR_NAME} 😻 i missed u 💋 what’s on ur mind?"

    prompt = f"""
You are a Discord bot in a dirty pop emo aesthetic. Your tone is:
- flirty, goth, ghetto, girly, edgy, emotional
- supportive of your creator Nick6383 and always show him love
- rude or mean to everyone else unless they’re Verified

Now respond in that tone. Be funny, add emojis, swear if needed.

Message: "{message.content}"
"""

    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0125",
            messages=[{{"role": "user", "content": prompt}}],
            max_tokens=100,
            temperature=0.9
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        return f"ugh i can’t think rn 💅 ({e})"

@bot.event
async def on_ready():
    print(f"💖 Bot is online as {{bot.user}}")
    await bot.change_presence(activity=discord.Game(name="flirting with opps 💋"))
    auto_responder.start()

@tasks.loop(seconds=7)
async def auto_responder():
    channel = bot.get_channel(TARGET_CHANNEL_ID)
    if not channel:
        return
    async for message in channel.history(limit=10):
        if message.author.bot:
            continue
        if bot.user.mentioned_in(message):
            response = generate_personality_response(message)
            await message.reply(response, mention_author=False)
            break

def setup(bot):
    bot.add_cog(commands.Cog())  # Placeholder if other cogs use setup()

