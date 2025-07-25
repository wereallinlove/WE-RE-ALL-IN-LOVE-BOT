# chat_moderation.py

import discord
from discord.ext import commands
import random
import re

BYPASS_ROLE_ID = 1371681883796017222

SLURS = [
    "retard", "tranny", "nigger", "nigga", "faggot", "dyke", "chink", "spic", "kike", "gook", "coon",
    "clanker", "cripple", "autist", "bitch", "twink", "shemale",
    "sandnigger", "towelhead"
]

BLOCKED_NAMES = ["patrick", "punkin", "punkinlove", "punkinloveee"]

CUTE_EMOJI_COMBOS = [
    "🧸💕🦄💖💟😜💝🕸️", "💫🐇🌸🩰🧁✨🌷💓", "🦋💐🧃💗🦢🫧🍧🪻", "🎀💖🍓💌🕊️💞🪩🌙",
    "🌈💜🌼🍒🦄🫶🐰💟", "💘🌺🪷🧸💅🏽🌸🫧👛", "🧁🌷💞🎀💖🫶🍓✨", "🧃🧚💫🪩💗🩵🌸🌼"
]

class ChatModeration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def has_bypass(self, member: discord.Member):
        return any(role.id == BYPASS_ROLE_ID for role in member.roles)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot or not message.guild:
            return

        member = message.author

        if self.has_bypass(member):
            return

        content_lower = message.content.lower()

        # Blocked names (no public message, DM only)
        if any(name in content_lower for name in BLOCKED_NAMES):
            try:
                await message.delete()
                await member.send("⚠️ Please do not mention that person again.")
            except:
                pass
            return

        # Slur filtering
        for slur in SLURS:
            pattern = r'\b' + re.escape(slur) + r'\b'
            if re.search(pattern, content_lower):
                try:
                    await message.delete()
                except:
                    pass

                emoji_combo = random.choice(CUTE_EMOJI_COMBOS)
                try:
                    await message.channel.send(f"{member.mention} keep it wholesome!! {emoji_combo}")
                except:
                    pass
                return

async def setup(bot):
    await bot.add_cog(ChatModeration(bot))