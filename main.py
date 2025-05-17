# main.py — slash command version only

import discord
from discord.ext import tasks
from discord import app_commands
import os

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

class BotClient(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.load_extension("music_commands")
        await self.load_extension("nick6383_trivia")
        await self.load_extension("verify_system")
        await self.tree.sync()
        print("✅ Slash commands synced")

client = BotClient()

@client.event
async def on_ready():
    print(f"🟢 Bot is ready. Logged in as {client.user}")

client.run(os.getenv("DISCORD_TOKEN"))
