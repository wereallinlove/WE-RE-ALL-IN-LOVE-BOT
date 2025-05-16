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
    await bot.tree.sync()
    print(f"Logged in as {bot.user}!")

# Load all modular command files
bot.tree.add_command(loveletter_command.loveletter)
bot.tree.add_command(pin_command.pin)
bot.tree.add_command(quote_command.quote)
bot.tree.add_command(daily_roast.roastnow)
bot.tree.add_command(nick6383_trivia.trivia)

# Start the verify system listener
verify_system.setup(bot)

if __name__ == "__main__":
    import asyncio

    async def main():
        async with bot:
            await bot.start(os.getenv("DISCORD_TOKEN"))

    asyncio.run(main())
