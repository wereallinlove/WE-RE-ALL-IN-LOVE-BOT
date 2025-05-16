import os
import discord
from discord.ext import commands, tasks
from discord.ui import Button, View
from discord.utils import get
from datetime import datetime
import asyncio

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=".", intents=intents)

ADMIN_CHANNEL_ID = 1318298515948048549
APPROVED_ROLE_NAME = "WE'RE ALL IN LOVE"
APPROVE_ROLE_NAME = ".approve"
VOICE_CHANNEL_ID = 137188628201131223

TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise ValueError("Bot token not found in environment variables.")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    hourly_bell.start()

@bot.event
async def on_member_join(member):
    await asyncio.sleep(1)  # short delay to prevent duplicate messages
    channel = bot.get_channel(ADMIN_CHANNEL_ID)
    if not channel:
        print("Admin channel not found.")
        return

    embed = discord.Embed(
        title="WE'RE ALL IN LOVE",
        description=f"{member.mention} joined\n\n**Grant them access to WE'RE ALL IN LOVE?**",
        color=discord.Color.purple()
    )

    button = Button(label="Approve", style=discord.ButtonStyle.success)

    async def button_callback(interaction):
        if APPROVE_ROLE_NAME not in [role.name for role in interaction.user.roles]:
            await interaction.response.send_message("You don't have permission to approve.", ephemeral=True)
            return

        role = discord.utils.get(member.guild.roles, name=APPROVED_ROLE_NAME)
        if role:
            await member.add_roles(role)
            await interaction.response.send_message(f"{member.mention} has been approved.", ephemeral=True)
        else:
            await interaction.response.send_message("Approval role not found.", ephemeral=True)

    button.callback = button_callback
    view = View()
    view.add_item(button)
    await channel.send(embed=embed, view=view)

@bot.command()
@commands.has_role(".admin")
async def bell(ctx):
    voice_channel = bot.get_channel(VOICE_CHANNEL_ID)
    if voice_channel and isinstance(voice_channel, discord.VoiceChannel):
        vc = await voice_channel.connect()
        vc.play(discord.FFmpegPCMAudio(source="bell.mp3"))
        while vc.is_playing():
            await asyncio.sleep(1)
        await vc.disconnect()
    else:
        await ctx.send("Voice channel not found.")

@tasks.loop(minutes=1)
async def hourly_bell():
    now = datetime.now()
    if now.minute == 0:  # On the hour
        voice_channel = bot.get_channel(VOICE_CHANNEL_ID)
        if voice_channel and isinstance(voice_channel, discord.VoiceChannel):
            vc = await voice_channel.connect()
            vc.play(discord.FFmpegPCMAudio(source="bell.mp3"))
            while vc.is_playing():
                await asyncio.sleep(1)
            await vc.disconnect()

bot.run(TOKEN)
