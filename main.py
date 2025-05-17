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
    await bot.load_extension("approve_command")
    await bot.load_extension("loveletter_command")
    await bot.load_extension("pin_command")  # This should match the filename without .py
    await bot.load_extension("quote_command")
    await bot.load_extension("nick6383_trivia")
    await bot.load_extension("daily_roast")
    print("✅ All extensions loaded. Syncing commands...")
    await bot.tree.sync()
    print("✅ Slash commands synced.")

bot.run(os.getenv("DISCORD_TOKEN"))
