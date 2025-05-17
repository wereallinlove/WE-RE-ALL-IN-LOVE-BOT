import discord
from discord.ext import commands
import os
import asyncio
import datetime

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

EXTENSIONS = [
    "pin_command",
    "nick6383_trivia",
    "music_commands",
    "loveletter_command",
    "quote_command",
    "daily_roast",
    "verify_system"
]

@bot.event
async def on_ready():
    print(f"Bot is ready. Logged in as {bot.user}")

@bot.event
async def setup_hook():
    for ext in EXTENSIONS:
        try:
            await bot.load_extension(ext)
            print(f"✅ Loaded {ext}")
        except Exception as e:
            print(f"❌ Failed to load {ext}: {e}")

    print("🔁 Syncing slash commands...")
    try:
        await bot.tree.sync()
        print("✅ Slash commands synced.")
    except Exception as e:
        print(f"❌ Slash command sync failed: {e}")

bot.run(os.getenv("DISCORD_TOKEN"))
