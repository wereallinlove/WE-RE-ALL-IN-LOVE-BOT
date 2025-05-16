import discord
from discord.ext import commands
import asyncio

# Import all your command and feature modules
import verify_system
import loveletter_command
import pin_command
import quote_command
import daily_roast
import nick6383_trivia

class MyBot(commands.Bot):
    async def setup_hook(self):
        await verify_system.setup(self)
        await loveletter_command.setup(self)
        await pin_command.setup(self)
        await quote_command.setup(self)
        await daily_roast.setup(self)
        await nick6383_trivia.setup(self)
        await self.tree.sync()  # sync globally so slash commands show up in all servers

intents = discord.Intents.all()
bot = MyBot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

bot.run("YOUR_DISCORD_TOKEN")
