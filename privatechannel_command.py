# privatechannel_command.py

import discord
from discord import app_commands
from discord.ext import commands, tasks
import asyncio
from datetime import datetime, timedelta

PRIVATE_ROLE_ID = 1396039656004653107
MEMBER_ROLE_ID = 1371885746415341648
CATEGORY_ID = 1395539999537238106
CHECK_INTERVAL = 30  # seconds

class PrivateChannel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_channels = {}  # {channel_id: {"owner": user_id, "timeout": datetime}}

    @app_commands.command(name="privatechannel", description="Create your own private voice channel.")
    @app_commands.checks.has_role(PRIVATE_ROLE_ID)
    async def privatechannel(self, interaction: discord.Interaction):
        user = interaction.user
        guild = interaction.guild
        category = guild.get_channel(CATEGORY_ID)

        # Name format
        channel_name = f"{user.display_name} · @{user.name}'s channel"
        
        # Permissions
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            guild.get_role(MEMBER_ROLE_ID): discord.PermissionOverwrite(view_channel=True, connect=False),
            user: discord.PermissionOverwrite(view_channel=True, connect=True, manage_channels=True, move_members=True),
        }

        # Create the channel
        channel = await guild.create_voice_channel(
            name=channel_name + " · 2m 0s left",
            overwrites=overwrites,
            category=category
        )

        # Track and start countdown
        end_time = datetime.utcnow() + timedelta(minutes=2)
        self.active_channels[channel.id] = {"owner": user.id, "timeout": end_time, "joined": False}
        asyncio.create_task(self._start_timer(channel, user, end_time))

        await interaction.response.send_message(f"✅ Created your private channel: {channel.mention}", ephemeral=True)

    async def _start_timer(self, channel, user, end_time):
        while True:
            if not await self.channel_exists(channel):
                return

            now = datetime.utcnow()
            remaining = (end_time - now).total_seconds()

            if remaining <= 0:
                await self._delete_channel(channel, user, "expired due to inactivity.")
                return

            # Check if owner joined
            voice_state = channel.guild.get_member(user.id)
            if voice_state and voice_state.voice and voice_state.voice.channel == channel:
                await channel.edit(name=f"{channel.name.split('·')[0]} · @{user.name}'s channel")
                self.active_channels[channel.id]["joined"] = True
                break

            # Update name
            mins, secs = divmod(int(remaining), 60)
            try:
                await channel.edit(name=f"{channel.name.split('·')[0]} · @{user.name}'s channel · {mins}m {secs:02d}s left")
            except:
                break

            await asyncio.sleep(CHECK_INTERVAL)

        # Start watching for owner leaving
        asyncio.create_task(self._watch_empty(channel, user))

    async def _watch_empty(self, channel, user):
        await asyncio.sleep(5)  # slight delay after join
        while True:
            if not await self.channel_exists(channel):
                return

            voice_state = channel.guild.get_member(user.id)
            if not voice_state or not voice_state.voice or voice_state.voice.channel != channel:
                # Owner left, start 2-minute deletion countdown
                end_time = datetime.utcnow() + timedelta(minutes=2)
                while True:
                    if not await self.channel_exists(channel):
                        return

                    # Owner rejoined
                    voice_state = channel.guild.get_member(user.id)
                    if voice_state and voice_state.voice and voice_state.voice.channel == channel:
                        await channel.edit(name=f"{channel.name.split('·')[0]} · @{user.name}'s channel")
                        break

                    now = datetime.utcnow()
                    remaining = (end_time - now).total_seconds()
                    if remaining <= 0:
                        await self._delete_channel(channel, user, "expired after you left.")
                        return

                    mins, secs = divmod(int(remaining), 60)
                    try:
                        await channel.edit(name=f"{channel.name.split('·')[0]} · @{user.name}'s channel · {mins}m {secs:02d}s left")
                    except:
                        break

                    await asyncio.sleep(CHECK_INTERVAL)

            await asyncio.sleep(5)

    async def _delete_channel(self, channel, user, reason):
        try:
            await channel.delete()
        except:
            return
        self.active_channels.pop(channel.id, None)

        # DM red embed
        try:
            embed = discord.Embed(
                title="❌ Private Channel Deleted",
                description=f"Your private voice channel was {reason}",
                color=discord.Color.red()
            )
            await user.send(embed=embed)
        except:
            pass  # can't DM user

    async def channel_exists(self, channel: discord.VoiceChannel):
        try:
            await channel.guild.fetch_channel(channel.id)
            return True
        except discord.NotFound:
            return False

async def setup(bot):
    await bot.add_cog(PrivateChannel(bot))
