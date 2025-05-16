import discord
from discord.ext import commands
import asyncio
import os

# Intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Bot setup
bot = commands.Bot(command_prefix="!", intents=intents)

# Load modular features
import verify_system
import pin_command
import quote_command
import daily_roast
import roast_joelle
import loveletter_command
import nick6383_trivia

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await bot.tree.sync()
    daily_roast.schedule_roasts(bot)

# Load each module’s commands
bot.tree.add_command(verify_system.approve)
bot.tree.add_command(verify_system.deny)
bot.tree.add_command(pin_command.pin)
bot.tree.add_command(quote_command.quote)
bot.tree.add_command(roast_joelle.roastjoelle)
bot.tree.add_command(loveletter_command.loveletter)
bot.tree.add_command(nick6383_trivia.nick6383trivia)
bot.tree.add_command(daily_roast.roastnow)

# Secure bot token loading
bot_token = os.getenv("DISCORD_TOKEN")
if bot_token is None:
    raise ValueError("DISCORD_TOKEN environment variable is not set.")
asyncio.run(bot.start(bot_token))
