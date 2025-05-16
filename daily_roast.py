import discord
from discord.ext import tasks
from discord import app_commands
import random
from datetime import datetime, time, timedelta
import asyncio

VERIFIED_ROLE_ID = 1371885746415341648
ADMIN_ROLE_ID = 1371681883796017222
ROAST_CHANNEL_ID = 1318298515948048549

roasts = [
    "Why are you even verified? Go touch grass.",
    "Certified loser detected. Try logging off.",
    "Your vibes are off. Permanently.",
    "I’ve seen bots with more personality than you.",
    "Congrats, you're today’s embarrassment.",
    "Imagine thinking anyone likes your messages.",
    "Your voice in VC makes people leave.",
    "You’re like a bug in the matrix — glitchy and annoying.",
    "You radiate ‘I peaked in 2017’ energy.",
    "They verified you by accident, right?"
]

def setup(bot):
    @bot.tree.command(name="roastnow", description="Roast a random verified user")
    async def roastnow(interaction: discord.Interaction):
        if ADMIN_ROLE_ID not in [role.id for role in interaction.user.roles]:
            await interaction.response.send_message("You don’t have permission to use this command.", ephemeral=True)
            return

        await interaction.response.defer(ephemeral=True)
        await send_roast(interaction.guild)
        await interaction.followup.send("Roast delivered.", ephemeral=True)

    @bot.event
    async def on_ready():
        if not roast_scheduler.is_running():
            roast_scheduler.start(bot)

@tasks.loop(hours=24)
async def roast_scheduler(bot):
    for guild in bot.guilds:
        await schedule_next_roast(bot, guild)

async def schedule_next_roast(bot, guild):
    now = datetime.now()

    # Time range: 7:00 AM to 1:00 AM the next day
    earliest = now.replace(hour=7, minute=0, second=0, microsecond=0)
    latest = (now + timedelta(days=1)).replace(hour=1, minute=0, second=0, microsecond=0)

    # Pick a random time in that range
    total_seconds = int((latest - earliest).total_seconds())
    random_seconds = random.randint(0, total_seconds)
    roast_time = earliest + timedelta(seconds=random_seconds)

    delay = (roast_time - now).total_seconds()
    print(f"[DAILY ROAST] Next roast scheduled at: {roast_time.strftime('%Y-%m-%d %I:%M %p')}")

    await asyncio.sleep(delay)
    await send_roast(guild)

async def send_roast(guild):
    channel = guild.get_channel(ROAST_CHANNEL_ID)
    if not channel:
        return

    verified_role = guild.get_role(VERIFIED_ROLE_ID)
    if not verified_role:
        return

    verified_members = [member for member in verified_role.members if not member.bot]
    if not verified_members:
        return

    target = random.choice(verified_members)
    roast = random.choice(roasts)

    await channel.send(f"{target.mention} {roast}")
