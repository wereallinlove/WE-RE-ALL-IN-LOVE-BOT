import discord
from discord.ext import commands, tasks
from discord.ui import Button, View
from discord.utils import get
import asyncio
import datetime
import os

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.guilds = True
intents.voice_states = True

bot = commands.Bot(command_prefix=".", intents=intents)

VC_CHANNEL_ID = 137188628201131223
ADMIN_CHANNEL_ID = 1318298515948048549
APPROVER_ROLE_NAME = ".approve"
ADMIN_ROLE_NAME = ".admin"
APPROVED_ROLE_NAME = "WE'RE ALL IN LOVE"
BELL_FILENAME = "bell.mp3"

# ============ JOIN EVENT / APPROVAL ============
class ApproveButton(Button):
    def __init__(self, member_id):
        super().__init__(label="Approve", style=discord.ButtonStyle.success, custom_id=f"approve:{member_id}")

    async def callback(self, interaction: discord.Interaction):
        if not any(role.name == APPROVER_ROLE_NAME for role in interaction.user.roles):
            await interaction.response.send_message("You don't have permission to approve.", ephemeral=True)
            return

        member_id = int(self.custom_id.split(":")[1])
        member = interaction.guild.get_member(member_id)
        role = get(interaction.guild.roles, name=APPROVED_ROLE_NAME)

        if member and role:
            await member.add_roles(role)
            await interaction.response.edit_message(content=f"{member.mention} has been approved ✅", embed=None, view=None)
        else:
            await interaction.response.send_message("Error approving member.", ephemeral=True)

class ApprovalView(View):
    def __init__(self, member_id):
        super().__init__(timeout=None)
        self.add_item(ApproveButton(member_id))

@bot.event
async def on_member_join(member):
    embed = discord.Embed(
        title="WE'RE ALL IN LOVE",
        description=f"{member.mention} joined.\n\n**Grant them access to WE'RE ALL IN LOVE?**",
        color=discord.Color.purple()
    )
    view = ApprovalView(member.id)
    channel = bot.get_channel(ADMIN_CHANNEL_ID)
    if channel:
        await channel.send(embed=embed, view=view)

# ============ PLAY BELL SOUND ============
async def play_bell(vc_channel):
    try:
        voice_client = await vc_channel.connect()
        audio = discord.FFmpegPCMAudio(BELL_FILENAME)
        voice_client.play(audio)
        while voice_client.is_playing():
            await asyncio.sleep(1)
        await voice_client.disconnect()
    except Exception as e:
        print(f"[ERROR] play_bell: {e}")

# ============ HOURLY BELL ============
@tasks.loop(minutes=1)
async def hourly_bell():
    now = datetime.datetime.utcnow()
    if now.minute == 0:
        guild = bot.guilds[0]
        vc = guild.get_channel(VC_CHANNEL_ID)
        await play_bell(vc)

# ============ .bell COMMAND ============
@bot.command()
async def bell(ctx):
    if any(role.name == ADMIN_ROLE_NAME for role in ctx.author.roles):
        vc = ctx.guild.get_channel(VC_CHANNEL_ID)
        await play_bell(vc)
        await ctx.send("🔔 Bell played.")
    else:
        await ctx.send("You do not have permission to use this.")

# ============ ON READY ============
@bot.event
async def on_ready():
    bot.add_view(ApprovalView(0))  # Register persistent view
    hourly_bell.start()
    print(f"✅ Logged in as {bot.user}")

# ============ RUN ============
bot.run(os.getenv("DISCORD_TOKEN"))
