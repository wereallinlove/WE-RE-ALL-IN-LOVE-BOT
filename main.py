import discord
from discord.ext import commands
import os
import verify_system
import loveletter_command
import pin_command
import quote_command
import daily_roast
import nick6383_trivia

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

    # Register slash commands
    try:
        await bot.tree.sync()
        print("Slash commands synced.")
    except Exception as e:
        print(f"Error syncing slash commands: {e}")

# Load all modular command files
verify_system.setup(bot)
loveletter_command.setup(bot)
pin_command.setup(bot)
quote_command.setup(bot)
daily_roast.setup(bot)
nick6383_trivia.setup(bot)

# Start bot
bot.run(os.getenv("DISCORD_TOKEN"))
