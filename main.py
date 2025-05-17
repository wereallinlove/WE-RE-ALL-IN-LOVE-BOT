import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.members = True
intents.guilds = True
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)
bot.tree.synced = False

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}!")
    if not bot.tree.synced:
        try:
            await bot.tree.sync()
            bot.tree.synced = True
            print("✅ Slash commands synced.")
        except Exception as e:
            print(f"Sync failed: {e}")

async def setup_hook():
    import verify_system
    import loveletter_command
    import pin_command
    import quote_command
    import daily_roast

    verify_system.setup(bot)
    loveletter_command.setup(bot)
    pin_command.setup(bot)
    quote_command.setup(bot)
    daily_roast.setup(bot)

    await bot.load_extension("nick6383_trivia")

bot.setup_hook = setup_hook

bot.run(os.getenv("DISCORD_TOKEN"))
