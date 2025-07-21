# beat_sorter.py

import discord
from discord.ext import commands
import re

CHAT_CHANNEL_ID = 1396937346619801752
BEATS_CHANNEL_ID = 1396937500697825310
LOOPS_CHANNEL_ID = 1396937593240948899

# Patterns
KEY_PATTERN = re.compile(r'\b([A-Ga-g](?:#|b)?(?:\s*(?:major|minor|harmonic minor)))\b', re.IGNORECASE)
BPM_PATTERN = re.compile(r'\b(\d{2,3})\b')

class BeatSorter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.channel.id != CHAT_CHANNEL_ID:
            return
        if message.author.bot or not message.attachments:
            return

        for attachment in message.attachments:
            filename = attachment.filename.lower()

            if not filename.endswith(('.mp3', '.wav', '.aiff', '.flac', '.ogg')):
                continue  # skip non-audio files

            if "beat" in filename:
                target_channel_id = BEATS_CHANNEL_ID
            elif "loop" in filename:
                target_channel_id = LOOPS_CHANNEL_ID
            else:
                try:
                    await message.delete()
                except:
                    pass
                await message.channel.send(
                    f"{message.author.mention} ⚠️ Please include the word **'beat'** or **'loop'** in your file name so it can be sorted.",
                    delete_after=8
                )
                return

            # Extract metadata
            key_match = KEY_PATTERN.search(filename)
            bpm_match = BPM_PATTERN.search(filename)

            key = key_match.group(1).title() if key_match else "Unknown"
            bpm = bpm_match.group(1) if bpm_match else "Unknown"

            # Forward message
            target_channel = self.bot.get_channel(target_channel_id)
            if target_channel:
                try:
                    file = await attachment.to_file()
                    embed = discord.Embed(
                        title="🎧 New Upload",
                        description=f"**From:** {message.author.mention}\n**Key:** {key}\n**BPM:** {bpm}",
                        color=discord.Color.purple()
                    )
                    await target_channel.send(embed=embed, file=file)
                except Exception as e:
                    print(f"[ERROR] Failed to forward file: {e}")
            try:
                await message.delete()
            except:
                pass

async def setup(bot):
    await bot.add_cog(BeatSorter(bot))