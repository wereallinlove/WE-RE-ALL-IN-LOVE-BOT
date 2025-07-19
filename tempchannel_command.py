# tempchannel_command.py

import discord
from discord import app_commands
from discord.ext import commands
import asyncio
from datetime import datetime, timedelta

class TempChannel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.temp_channels = {}

    @app_commands.command(name="tempchannel", description="Clone a voice channel temporarily with a live timer.")
    @app_commands.checks.has_role(1396035218896584714)
    async def tempchannel(self, interaction: discord.Interaction, minutes: app_commands.Range[int, 1, 120]):
        original_channel = interaction.guild.get_channel(1371886282011312231)

        if not original_channel or not isinstance(original_channel, discord.VoiceChannel):
            await interaction.response.send_message("Original voice channel not found or is invalid.", ephemeral=True)
            return

        # Clone the channel
        cloned_channel = await original_channel.clone()
        end_time = datetime.utcnow() + timedelta(minutes=minutes)

        async def update_name():
            while True:
                remaining = int((end_time - datetime.utcnow()).total_seconds() // 60)
                if remaining <= 0:
                    break
                new_name = f"{original_channel.name} · temporary channel · {remaining}m left"
                await cloned_channel.edit(name=new_name)
                await asyncio.sleep(60)

        await interaction.response.send_message(
            f"✅ Temporary voice channel created: {cloned_channel.mention} (for {minutes} minutes)",
            ephemeral=True
        )

        # Start name updater
        asyncio.create_task(update_name())

        # Wait for expiration
        await asyncio.sleep(minutes * 60)

        # Delete the channel if it still exists
        if cloned_channel and await self.channel_exists(cloned_channel):
            await cloned_channel.delete()

    async def channel_exists(self, channel: discord.VoiceChannel):
        try:
            await channel.guild.fetch_channel(channel.id)
            return True
        except discord.NotFound:
            return False

async def setup(bot):
    await bot.add_cog(TempChannel(bot))
