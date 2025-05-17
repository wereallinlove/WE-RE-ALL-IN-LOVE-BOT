# main.py — updated with slash command sync and working extension loading

import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

EXTENSIONS = [
    "verify_system",
    "music_commands",
    "nick6383_trivia"
]

@bot.event
async def setup_hook():
    for ext in EXTENSIONS:
        try:
            await bot.load_extension(ext)
            print(f"✅ Loaded {ext}")
        except Exception as e:
            print(f"❌ Failed to load {ext}: {e}")
    await bot.tree.sync()
    print("✅ Slash commands synced")

@bot.event
async def on_ready():
    print(f"🟢 Bot is ready. Logged in as {bot.user}")

bot.run(os.getenv("DISCORD_TOKEN"))