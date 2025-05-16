import os
import discord
from discord.ext import commands, tasks
from discord.ui import Button, View
from datetime import datetime
import asyncio

# Load .env variables (in Railway they’re already set)
TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN or TOKEN == "":  # Failsafe
    print("❌ DISCORD_TOKEN is missing or not loaded.")
    exit()

# Setup bot
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix=".", intents=intents)

# Roles & Channels
ADMIN_CHANNEL_ID = 1318298515948048549
APPROVE_ROLE_NAME = "WE'RE ALL IN LOVE"
VOICE_CHANNEL_ID = 137188628201131223
APPROVER_ROLE_NAME = ".approve"

# On ready
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    hourly_bell.start()

# Member joins
@bot.event
async def on_member_join(member):
    channel = bot.get_channel(ADMIN_CHANNEL_ID)
    if not channel:
        print("❌ Admin channel not found.")
        return

    embed = discord.Embed(
        title="WE'RE ALL IN LOVE",
        description=f"{member.mention} joined. **Grant them access to WE'RE ALL IN LOVE?**",
        color=0xAA00AA
    )

    button = Button(label="Approve", style=discord.ButtonStyle.success)

    async def approve_callback(interaction):
        if not any(role.name == APPROVER_ROLE_NAME for role in interaction.user.roles):
            await interaction.response.send_message("❌ You don’t have permission to approve.", ephemeral=True)
            return

        role = discord.utils.get(member.guild.roles, name=APPROVE_ROLE_NAME)
        if role:
            await member.add_roles(role)
            await interaction.response.send_message(f"✅ {member.mention} has been approved.", ephemeral=False)
        else:
            await interaction.response.send_message("❌ Role not found.", ephemeral=True)

    button.callback = approve_callback
    view = View()
    view.add_item(button)

    await channel.send(embed=embed, view=view)

# Command: .bell
@bot.command()
async def bell(ctx):
    if not any(role.name == ".admin" for role in ctx.author.roles):
        await ctx.send("❌ You don't have permission.")
        return

    vc = ctx.author.voice
    if not vc:
        await ctx.send("⚠️ You must be in a voice channel.")
        return

    voice = await vc.channel.connect()
    voice.play(discord.FFmpegPCMAudio("bell.mp3"))
    while voice.is_playing():
        await asyncio.sleep(1)
    await voice.disconnect()

# Automatic hourly bell
@tasks.loop(minutes=1)
async def hourly_bell():
    now = datetime.now()
    if now.minute == 0:
        guild = bot.guilds[0]
        channel = discord.utils.get(guild.voice_channels, id=VOICE_CHANNEL_ID)
        if channel:
            voice = await channel.connect()
            voice.play(discord.FFmpegPCMAudio("bell.mp3"))
            while voice.is_playing():
                await asyncio.sleep(1)
            await voice.disconnect()

# Run bot
bot.run(TOKEN)
