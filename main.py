import discord
from discord.ext import commands
import os

GUILD_ID = 1318298515948048546

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print("🧨 Connected. Wiping ALL slash commands...")

    # Wipe GLOBAL commands
    global_commands = await bot.tree.fetch()
    for cmd in global_commands:
        print(f"🗑 Deleting GLOBAL: {cmd.name}")
        await bot.http.delete_global_command(cmd.id)

    # Wipe GUILD commands
    guild = discord.Object(id=GUILD_ID)
    guild_commands = await bot.tree.fetch(guild=guild)
    for cmd in guild_commands:
        print(f"🗑 Deleting GUILD: {cmd.name}")
        await bot.http.delete_guild_command(bot.application_id, GUILD_ID, cmd.id)

    print("✅ All slash commands (global + guild) deleted.")
    await bot.close()

bot.run(os.getenv("DISCORD_TOKEN"))
