import discord
from discord.ext import commands, tasks
from discord.ui import Button, View
from discord.utils import get
import os
import asyncio
import datetime

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.guilds = True
intents.voice_states = True

bot = commands.Bot(command_prefix=".", intents=intents)

# === CONFIG ===
ADMIN_CHANNEL_ID = 1318298515948048549  # where the approval embed is sent
APPROVED_ROLE_NAME = "WE'RE ALL IN LOVE"
APPROVER_ROLE_NAME = ".approve"
VC_CHANNEL_ID = 137188628201131223
ADMIN_ROLE_NAME = ".admin"
SOUND_URL = "https://srv-store3.gofile.io/download/wc3h3c/chime.mp3"

# === Prevent double join messages ===
recent_joins = set()

# === APPROVAL BUTTON ===
class ApproveButton(Button):
    def __init__(self, member_id):
        super().__init__(label="Approve", style=discord.ButtonStyle.success, custom_id=f"approve:{member_id}")

    async def callback(self, interaction: discord.Interaction):
        approver_role = discord.utils.get(interaction.user.roles, name=APPROVER_ROLE_NAME)
        if not approver_role:
            await interaction.response.send_message("You must have the `.approve` role to approve members.", ephemeral=True)
            return

        member_id = int(self.custom_id.split(":")[1])
        guild = interaction.guild
        member = guild.get_member(member_id)
        if not member:
            await interaction.response.send_message("Could not find the member to approve.", ephemeral=True)
            return

        role = discord.utils.get(guild.roles, name=APPROVED_ROLE_NAME)
        if not role:
            await interaction.response.send_message("Approved role not found.", ephemeral=True)
            return

        await member.add_roles(role)
        await interaction.response.edit_message(
            content=f"{member.mention} has been approved and given the role '{role.name}'.",
            embed=None,
            view=None
        )

class ApprovalView(View):
    def __init__(self, member_id):
        super().__init__(timeout=None)
        self.add_item(ApproveButton(member_id))

# === ON READY ===
@bot.event
async def on_ready():
    bot.add_view(ApprovalView(0))  # required to register persistent view
    print(f"Logged in as {bot.user}")
    hourly_chime.start()

# === ON MEMBER JOIN ===
@bot.event
async def on_member_join(member):
    if member.id in recent_joins:
        return

    recent_joins.add(member.id)
    await asyncio.sleep(5)
    recent_joins.remove(member.id)

    channel = bot.get_channel(ADMIN_CHANNEL_ID)
    if not channel:
        print("Admin channel not found.")
        return

    embed = discord.Embed(
        title="WE'RE ALL IN LOVE",
        description=f"{member.mention} joined the server.\n\nGrant them access to **WE'RE ALL IN LOVE**?",
        color=discord.Color.purple()
    )

    await channel.send(embed=embed, view=ApprovalView(member.id))

# === CHIME FUNCTION ===
async def play_chime(vc_channel):
    try:
        if not vc_channel:
            print("Voice channel not found.")
            return

        voice_client = await vc_channel.connect()
        source = await discord.FFmpegOpusAudio.from_probe(SOUND_URL, method='fallback')
        voice_client.play(source)

        while voice_client.is_playing():
            await asyncio.sleep(1)

        await voice_client.disconnect()

    except Exception as e:
        print(f"Error in play_chime: {e}")

# === HOURLY TASK ===
@tasks.loop(minutes=1)
async def hourly_chime():
    now = datetime.datetime.now()
    if now.minute == 0:
        guild = discord.utils.get(bot.guilds)
        if guild:
            vc_channel = guild.get_channel(VC_CHANNEL_ID)
            await play_chime(vc_channel)

# === MANUAL COMMAND ===
@bot.command()
async def chime(ctx):
    if get(ctx.author.roles, name=ADMIN_ROLE_NAME):
        vc_channel = ctx.guild.get_channel(VC_CHANNEL_ID)
        await play_chime(vc_channel)
        await ctx.send("Chime activated.")
    else:
        await ctx.send("You do not have permission to use this command.")

# === KEEP ALIVE (if needed) ===
from keep_alive import keep_alive
keep_alive()

bot.run(os.getenv("TOKEN"))
