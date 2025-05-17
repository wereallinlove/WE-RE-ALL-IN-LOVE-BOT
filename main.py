import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

EXTENSIONS = []  # Leave empty to prevent registering commands

@bot.event
async def on_ready():
    print(f"Bot is online: {bot.user}")

@bot.event
async def setup_hook():
    print("Skipping slash command sync (wiping mode).")

bot.run(os.getenv("DISCORD_TOKEN"))
