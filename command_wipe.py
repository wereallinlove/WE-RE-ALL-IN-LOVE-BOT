import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print("🔨 Connected. Deleting all application commands...")
    app_commands = await bot.tree.fetch()
    for cmd in app_commands:
        print(f"Deleting: {cmd.name}")
        await bot.http.delete_global_command(cmd.id)
    print("✅ All application commands deleted.")
    await bot.close()

bot.run(os.getenv("DISCORD_TOKEN"))
