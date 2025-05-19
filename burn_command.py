import discord
from discord import app_commands
from discord.ext import commands
import random

BURN_ROLE_ID = 1371885746415341648
BURN_CHANNEL_ID = 1318298515948048549
EMBED_COLOR = discord.Color.from_rgb(231, 84, 128)  # pink

FAKE_BURNS = [
    "i write fanfic about people in this server",
    "sometimes i bark at my mirror and hope it barks back",
    "i fake cry during arguments to win",
    "i lied about finishing therapy",
    "i made an alt just to stalk my ex's playlist",
    "i unironically simp for ai vtubers",
    "i ate ice out of the urinal in 2nd grade",
    "i keep fake screenshots in my gallery just in case",
    "i meow in voice chats when i’m nervous",
    "i used a ouija board to ask if they liked me back",
    "i got banned from a roblox server for ERP",
    "i call my crushes 'master' in my Notes app",
    "i still check my ex's spotify blend every day",
    "i save their selfies and pretend we’re dating",
    "i sent myself anons and pretended they were real",
    "i made a shrine to someone in minecraft",
    "i fake laugh in vc hoping they’ll fall in love",
    "i dream about being owned by them",
    "i wrote a poem about their typing style",
    "i gaslight myself for fun",
    "i have a list of everyone who ignored my dm",
    "i fake sleep in vc just to hear them talk",
    "i changed my birthday to match theirs",
    "i once tried to astral project into their bedroom",
    "i learned their timezone so i could 'accidentally' be online",
    "i used tarot cards to check if we’re soulmates",
    "i fantasize about being blocked by them",
    "i once roleplayed as their dead dog to get attention",
    "i edited their face onto my lockscreen background",
    "i rewatch their deleted stories like it’s cinema",
    "i whispered their name during a test",
    "i saved every 'typing...' moment they gave me",
    "i’d let them destroy me emotionally just to feel alive",
    "i said 'love u' and unsent it just to see if they noticed",
    "i wore their hoodie and cried while biting the sleeve",
    "i liked their comment from 2021. on purpose.",
    "i’d crawl into their walls if given the chance",
    "i miss people who never knew i existed",
    "i used to send cursed images to get their attention",
    "i planned our wedding before we even talked",
    "i recorded them in vc and looped it",
    "i used a sock puppet account to flirt with them",
    "i fake confidence hoping they’ll notice me",
    "i put my phone on airplane mode after texting to manifest a reply",
    "i tried to curse their partner with a pinterest spell",
    "i stole their pfps to pretend we matched",
    "i use their quotes as my status and pretend they’re mine",
    "i once cried when they liked someone else's message",
    "i keep logs of our interactions like it's the bible",
    "i want them to yell at me but also hold me after",
    "i tried to clone their spotify taste to feel closer",
    "i screenshot every time they say my name",
    "i lied about watching that movie just to talk to them",
    "i once roleplayed as their future partner in my journal",
    "i keep rereading a 'lol' they sent 3 days ago",
    "i learned tarot just to pull cards about them",
    "i once meowed mid-call and blamed lag",
    "i overanalyze their emojis like they’re prophecies",
    "i made an edit of us and never posted it",
    "i listen to songs they liked on repeat to suffer better",
    "i wrote their @ in cursive 32 times on a post-it note",
    "i told my therapist about them. multiple times.",
    "i said i moved on. i lied.",
]

class Burn(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="burn", description="Forge a fake embarrassing Discord screenshot.")
    @app_commands.checks.has_role(BURN_ROLE_ID)
    async def burn(self, interaction: discord.Interaction, user: discord.Member):
        if interaction.channel.id != BURN_CHANNEL_ID:
            await interaction.response.send_message("You can only burn people in the designated channel.", ephemeral=True)
            return

        line = random.choice(FAKE_BURNS)
        embed = discord.Embed(
            description=f"**{user.display_name}:** {line}",
            color=EMBED_COLOR
        )
        embed.set_thumbnail(url=user.display_avatar.url)
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Burn(bot))
