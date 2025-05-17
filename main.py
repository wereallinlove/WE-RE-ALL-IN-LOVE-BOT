import discord
from discord.ext import commands
import os
import asyncio
import datetime

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot is ready. Logged in as {bot.user}")

@bot.event
async def setup_hook():
    # Load all your feature files
    await bot.load_extension("pin_command")
    await bot.load_extension("nick6383_trivia")
    await bot.load_extension("music_commands")
    await bot.load_extension("loveletter_command")
    await bot.load_extension("quote_command")
    await bot.load_extension("daily_roast")
    await bot.load_extension("verify_system")
    print("✅ Loaded all extensions. Syncing slash commands...")
    await bot.tree.sync()
    print("✅ Slash commands synced.")

bot.run(os.getenv("DISCORD_TOKEN"))
