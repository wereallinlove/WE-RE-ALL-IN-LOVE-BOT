import discord
from discord.ext import commands, tasks
from discord.ui import Button, View
import asyncio
import os

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=".", intents=intents)

ADMIN_CHANNEL_ID = 1318298515948048549
APPROVED_ROLE_NAME = "WE'RE ALL IN LOVE"
VC_CHANNEL_ID = 137188628201131223

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    hourly_bell.start()

@bot.event
async def on_member_join(member):
    await asyncio.sleep(1)
    channel = bot.get_channel(ADMIN_CHANNEL_ID)
    if not channel:
        print("Admin channel not found.")
        return

    embed = discord.Embed(
        title="WE'RE ALL IN LOVE",
        description=f"{member.mention} joined the server.\n\n**Grant them access to WE'RE ALL IN LOVE?**",
        color=discord.Color.purple()
    )

    async def approve_callback(interaction):
        approver = interaction.user
        if any(role.name == ".approve" for role in approver.roles):
            role = discord.utils.get(member.guild.roles, name=APPROVED_ROLE_NAME)
            if role:
                await member.add_roles(role)
                await interaction.response.send_message(f"{member.mention} has been approved by {approver.mention}.", ephemeral=False)
            else:
                await interaction.response.send_message("Approval role not found.", ephemeral=True)
        else:
            await interaction.response.send_message("You do not have permission to approve members.", ephemeral=True)

    button = Button(label="Approve", style=discord.ButtonStyle.success)
    button.callback = approve_callback
    view = View()
    view.add_item(button)
    await channel.send(embed=embed, view=view)

# ────────────────────────────────────────────────
# .bell Command (Admin Only)
# ────────────────────────────────────────────────
@bot.command()
async def bell(ctx):
    if any(role.name == ".admin" for role in ctx.author.roles):
        vc = ctx.guild.get_channel(VC_CHANNEL_ID)
        if vc:
            try:
                voice = await vc.connect()
                audio_source = discord.FFmpegPCMAudio("bell.mp3")
                voice.play(audio_source)

                while voice.is_playing():
                    await asyncio.sleep(1)

                await voice.disconnect()
                await ctx.send("🔔 Bell has been rung.")
            except Exception as e:
                await ctx.send(f"Error: {e}")
        else:
            await ctx.send("Voice channel not found.")
    else:
        await ctx.send("You don't have permission to use this command.")

# ────────────────────────────────────────────────
# Hourly Bell Task (Every Hour on the Hour)
# ────────────────────────────────────────────────
@tasks.loop(minutes=1)
async def hourly_bell():
    now = discord.utils.utcnow()
    if now.minute == 0:
        guild = bot.guilds[0]
        vc = guild.get_channel(VC_CHANNEL_ID)
        if vc:
            try:
                voice = await vc.connect()
                audio_source = discord.FFmpegPCMAudio("bell.mp3")
                voice.play(audio_source)

                while voice.is_playing():
                    await asyncio.sleep(1)

                await voice.disconnect()
                print("🔔 Hourly bell played.")
            except Exception as e:
                print(f"Error playing hourly bell: {e}")

bot.run(os.getenv("TOKEN"))
