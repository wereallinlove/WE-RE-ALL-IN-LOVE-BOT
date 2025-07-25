# hourly_bell.py

import discord
from discord.ext import commands, tasks
import asyncio
import datetime

VC_DEFAULT_ID = 1371886282011312231

class HourlyBell(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.play_bell.start()

    def cog_unload(self):
        self.play_bell.cancel()

    @tasks.loop(minutes=1)
    async def play_bell(self):
        now = datetime.datetime.now()
        if now.minute != 0:
            return  # only run at the start of each hour

        for guild in self.bot.guilds:
            try:
                # If already in VC, skip to avoid music conflict
                if guild.voice_client and guild.voice_client.is_connected():
                    return

                # Step 1: Try default VC
                default_channel = guild.get_channel(VC_DEFAULT_ID)
                target_channel = None

                if default_channel and len(default_channel.members) > 0:
                    target_channel = default_channel
                else:
                    # Step 2: Find other VC with most people
                    voice_channels = [c for c in guild.voice_channels if len(c.members) > 0]
                    if voice_channels:
                        target_channel = max(voice_channels, key=lambda c: len(c.members))

                if not target_channel:
                    return  # nobody online

                vc = await target_channel.connect()
                source = discord.FFmpegPCMAudio("bell.mp3", options='-filter:a "volume=2.0"')  # Loud bell
                vc.play(source)

                while vc.is_playing():
                    await asyncio.sleep(1)

                await vc.disconnect()

            except Exception as e:
                print(f"[Hourly Bell Error] {e}")

    @play_bell.before_loop
    async def before_bell(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(HourlyBell(bot))