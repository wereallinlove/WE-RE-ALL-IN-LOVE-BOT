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
    "verify_system",
    "music_commands"
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

    print("🔁 Syncing slash commands to GUILD_ID 1318298515948048546 for fast updates...")
    try:
        guild = discord.Object(id=1318298515948048546)
        await bot.tree.sync(guild=guild)
        print("✅ Slash commands synced to your server.")
    except Exception as e:
        print(f"❌ Slash command sync failed: {e}")

bot.run(os.getenv("DISCORD_TOKEN"))
