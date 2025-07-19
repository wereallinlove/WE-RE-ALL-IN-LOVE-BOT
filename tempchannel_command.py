# tempchannel_command.py

import discord
from discord import app_commands
from discord.ext import commands
import asyncio
from datetime import datetime, timedelta

# Configuration
ALLOWED_ROLE_ID = 1396035218896584714
SOURCE_CHANNEL_ID = 1371886282011312231
MAX_TEMP_CHANNELS = 5

class TempChannel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.temp_channels = []

    @app_commands.command(name="tempchannel", description="Clone a voice channel temporarily with a live countdown.")
    @app_commands.checks.has_role(ALLOWED_ROLE_ID)
    async def tempchannel(self, interaction: discord.Interaction, minutes: app_commands.Range[int, 1, 120]):
        # Check limit
        if len(self.temp_channels) >= MAX_TEMP_CHANNELS:
            await interaction.response.send_message(
                f"⚠️ There are already {MAX_TEMP_CHANNELS} temporary voice channels active. Please wait until one closes.",
                ephemeral=True
            )
            return

        source_channel = interaction.guild.get_channel(SOURCE_CHANNEL_ID)
        if not source_channel or not isinstance(source_channel, discord.VoiceChannel):
            await interaction.response.send_message("❌ Original voice channel not found.", ephemeral=True)
            return

        # Clone the channel
        end_time = datetime.utcnow() + timedelta(minutes=minutes)
        cloned_channel = await source_channel.clone()
        self.temp_channels.append(cloned_channel.id)

        # Update loop every 30 seconds
        async def update_channel_name():
            while True:
                remaining_seconds = int((end_time - datetime.utcnow()).total_seconds())
                if remaining_seconds <= 0:
                    break
                mins, secs = divmod(remaining_seconds, 60)
                new_name = f"{source_channel.name} · temporary channel · {mins}m {secs:02d}s left"
                try:
                    await cloned_channel.edit(name=new_name)
                except:
                    break  # Likely deleted or no perms
                await asyncio.sleep(30)

        await interaction.response.send_message(
            f"✅ Created temporary voice channel: {cloned_channel.mention} for {minutes} minutes.",
            ephemeral=True
        )

        # Start updating
        asyncio.create_task(update_channel_name())

        # Wait until deletion time
        await asyncio.sleep(minutes * 60)

        if await self.channel_exists(cloned_channel):
            try:
                await cloned_channel.delete()
                self.temp_channels.remove(cloned_channel.id)

                # Send red embed
                embed = discord.Embed(
                    title="⏳ Temp Channel Deleted",
                    description=f"The channel **{source_channel.name} · temporary channel** expired after {minutes} minutes.",
                    color=discord.Color.red()
                )
                await interaction.channel.send(embed=embed)
            except:
                pass

    async def channel_exists(self, channel: discord.VoiceChannel):
        try:
            await channel.guild.fetch_channel(channel.id)
            return True
        except discord.NotFound:
            return False

async def setup(bot):
    await bot.add_cog(TempChannel(bot))
