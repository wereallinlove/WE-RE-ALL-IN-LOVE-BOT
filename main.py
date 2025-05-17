import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

EXTENSIONS = [
    "verify_system",
    "music_commands",
    "nick6383_trivia"
]

@bot.event
async def on_ready():
    print(f"🎉 Bot is ready. Logged in as {bot.user}")

@bot.event
async def setup_hook():
    for ext in EXTENSIONS:
        try:
            await bot.load_extension(ext)
            print(f"✅ Loaded {ext}")
        except Exception as e:
            print(f"❌ Failed to load {ext}: {e}")

bot.run(os.getenv("DISCORD_TOKEN"))
