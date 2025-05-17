import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print("🔨 Connected. Deleting all global application commands...")
    commands_list = await bot.tree.fetch()
    for cmd in commands_list:
        print(f"Deleting: {cmd.name}")
        await bot.http.delete_global_command(cmd.id)
    print("✅ All global slash commands deleted.")
    await bot.close()

bot.run(os.getenv("DISCORD_TOKEN"))
