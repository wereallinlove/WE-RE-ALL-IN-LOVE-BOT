import discord
from discord.ext import tasks
from discord import app_commands
import random
from datetime import datetime, timedelta
import asyncio

VERIFIED_ROLE_ID = 1371885746415341648
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
    "They verified you by accident, right?",
    "Minecraft isn't a personality trait. Let it go.",
    "Dead by Daylight called—they want their toxicity back.",
    "You build like you PvP: slow, confused, and embarrassing.",
    "Your Spotify Wrapped was a cry for help.",
    "‘Indie’ doesn’t mean boring. You just have bad taste.",
    "How are you verified and still invisible?",
    "Every time you speak in VC, a kitten dies.",
    "Your messages drop server morale by 20%.",
    "You're not misunderstood. You're just weird.",
    "You make Minecraft look like a horror game.",
    "Your favorite band peaked on SoundCloud in 2013.",
    "You’re the reason lobbies go silent.",
    "You play DBD like it’s your therapy session.",
    "You’re the human version of a cooldown timer.",
    "If cringe was currency, you'd be rich.",
    "Your vibe is free trial energy.",
    "You say ‘it’s just a game’ because you’re always losing.",
    "Every playlist you send is just sad noise.",
    "You're the NPC everyone skips.",
    "Your presence lowers the server's K/D.",
    "Even your ghost pings are mid.",
    "You're one more message away from getting ratio’d.",
    "You play Minecraft like it’s competitive esports. Relax.",
    "You remind me of a patch note nobody read.",
    "You bring less to the table than a lag spike.",
    "You argue in VC like it’s a TED talk. Shut up.",
    "You sound like an off-brand Lo-Fi stream.",
    "Your music taste says ‘emotionally unavailable’.",
    "You look like you get booted from every group chat.",
    "Your DBD perks are as weak as your personality.",
    "You're a walking disconnect.",
    "If awkward was a vibe, you’d be the whole playlist.",
    "Even Clippy couldn’t help you socially.",
    "Your digital footprint is just emotional damage.",
    "You're not quirky. You're annoying.",
    "Everyone zones out when you talk.",
    "You radiate controller drift energy.",
    "Even AI doesn't want to chat with you.",
    "You're like a group project partner who never shows up.",
    "fuck you.",
    "You call that a meme? Delete it.",
    "Your presence is like a pop-up ad: loud and unnecessary.",
    "You act like a main character with side quest energy.",
    "You bring passive-aggressive aura to every lobby."
]

def setup(bot):
    @bot.tree.command(name="roastnow", description="Roast a random verified user")
    async def roastnow(interaction: discord.Interaction):
        if VERIFIED_ROLE_ID not in [role.id for role in interaction.user.roles]:
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
        await schedule_three_roasts(bot, guild)

async def schedule_three_roasts(bot, guild):
    now = datetime.now()
    base = now.replace(hour=7, minute=0, second=0, microsecond=0)
    end = (now + timedelta(days=1)).replace(hour=1, minute=0, second=0, microsecond=0)

    total_range = int((end - base).total_seconds())

    # Choose 3 unique times
    delays = sorted(random.sample(range(total_range), 3))
    for seconds in delays:
        roast_time = base + timedelta(seconds=seconds)
        delay = (roast_time - datetime.now()).total_seconds()
        print(f"[DAILY ROAST] Scheduled roast at {roast_time.strftime('%Y-%m-%d %I:%M %p')}")
        await asyncio.sleep(delay)
        await send_roast(guild)

async def send_roast(guild):
    channel = guild.get_channel(ROAST_CHANNEL_ID)
    if not channel:
        return

    verified_role = guild.get_role(VERIFIED_ROLE_ID)
    if not verified_role:
        return

    verified_members = [m for m in verified_role.members if not m.bot]
    if not verified_members:
        return

    target = random.choice(verified_members)
    roast = random.choice(roasts)

    await channel.send(f"{target.mention} {roast}")
