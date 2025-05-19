# main.py — fixed version using commands.Bot with slash support

import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"🟢 Bot is ready. Logged in as {bot.user}")
    print("✅ Slash commands synced")

EXTENSIONS = [
    "verify_system",
    "music_commands",
    "nick6383_trivia",
    "roast_joelle",
    "roast_valentine",
    "loveletter",
    "quote_command",
    "clips",
    "fight_command",
    "duel_command",
    "nick6383_triviaduel",
    "expose_command"
]

@bot.event
async def setup_hook():
    for ext in EXTENSIONS:
        try:
            await bot.load_extension(ext)
            print(f"✅ Loaded {ext}")
        except Exception as e:
            print(f"❌ Failed to load {ext}: {e}")

bot.run(os.getenv("DISCORD_TOKEN"))
