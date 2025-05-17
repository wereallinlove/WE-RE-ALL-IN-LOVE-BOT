import discord
from discord.ext import commands
import os
import asyncio
import datetime

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

EXTENSIONS = []  # TEMP: No extensions loaded to force Discord to clear slash commands

@bot.event
async def on_ready():
    print(f"🎉 Bot is ready. Logged in as {bot.user}")

@bot.event
async def setup_hook():
    print("🧹 Clearing ALL slash commands from the server (temporary sync)...")
    try:
        guild = discord.Object(id=1318298515948048546)
        bot.tree.clear_commands(guild=guild)
        await bot.tree.sync(guild=guild)
        print("✅ All commands removed from the server.")
    except Exception as e:
        print(f"❌ Slash command clearing failed: {e}")

bot.run(os.getenv("DISCORD_TOKEN"))
