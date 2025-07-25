# hourly_bell.py

import discord
from discord.ext import commands, tasks
from discord import app_commands
import asyncio
import datetime

VC_DEFAULT_ID = 1371886282011312231
ADMIN_ROLE_ID = 1371681883796017222

class HourlyBell(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.play_bell_loop.start()

    def cog_unload(self):
        self.play_bell_loop.cancel()

    @tasks.loop(minutes=1)
    async def play_bell_loop(self):
        now = datetime.datetime.now()
        if now.minute != 0:
            return  # Only at the top of the hour

        for guild in self.bot.guilds:
            if guild.voice_client and guild.voice_client.is_connected():
                continue  # Skip if already playing something (like music)

            await self._play_bell(guild)

    @play_bell_loop.before_loop
    async def before_bell(self):
        await self.bot.wait_until_ready()

    async def _play_bell(self, guild: discord.Guild):
        try:
            # Pick VC with most people, fallback to default
            voice_channels = [c for c in guild.voice_channels if len(c.members) > 0]
            target_channel = max(voice_channels, key=lambda c: len(c.members), default=None)

            if not target_channel:
                target_channel = guild.get_channel(VC_DEFAULT_ID)

            if not target_channel:
                return  # No valid channel

            vc = await target_channel.connect()
            source = discord.FFmpegPCMAudio("bell.mp3", options='-filter:a "volume=2.0"')  # Louder
            vc.play(source)

            while vc.is_playing():
                await asyncio.sleep(1)

            await vc.disconnect()

        except Exception as e:
            print(f"[Hourly Bell Error] {e}")

    # Manual command: /bell
    @app_commands.command(name="bell", description="Manually test the church bell sound.")
    @app_commands.checks.has_role(ADMIN_ROLE_ID)
    async def bell(self, interaction: discord.Interaction):
        await interaction.response.send_message("🔔 Playing church bell...", ephemeral=True)
        await self._play_bell(interaction.guild)

async def setup(bot):
    await bot.add_cog(HourlyBell(bot))