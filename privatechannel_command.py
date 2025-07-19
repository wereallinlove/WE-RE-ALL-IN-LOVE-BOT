# privatechannel_command.py

import discord
from discord import app_commands
from discord.ext import commands
import asyncio
from datetime import datetime, timedelta

PRIVATE_ROLE_ID = 1396039656004653107
MEMBER_ROLE_ID = 1371885746415341648
CATEGORY_ID = 1395539999537238106
CHECK_INTERVAL = 60  # now 1 minute instead of 30 seconds

class PrivateChannel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_channels = {}

    @app_commands.command(name="privatechannel", description="Create your own private voice channel.")
    @app_commands.checks.has_role(PRIVATE_ROLE_ID)
    async def privatechannel(self, interaction: discord.Interaction):
        user = interaction.user
        guild = interaction.guild
        category = guild.get_channel(CATEGORY_ID)

        base_name = f"{user.display_name} · @{user.name}'s channel"
        full_name = base_name + " · 2m 0s left"

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            guild.get_role(MEMBER_ROLE_ID): discord.PermissionOverwrite(view_channel=True, connect=False),
            user: discord.PermissionOverwrite(view_channel=True, connect=True, manage_channels=True, move_members=True),
        }

        channel = await guild.create_voice_channel(
            name=full_name,
            overwrites=overwrites,
            category=category
        )

        end_time = datetime.utcnow() + timedelta(minutes=2)
        self.active_channels[channel.id] = {"owner": user.id, "timeout": end_time, "joined": False}
        asyncio.create_task(self._start_timer(channel, user, end_time, base_name))

        await interaction.response.send_message(f"✅ Created your private channel: {channel.mention}", ephemeral=True)

    async def _start_timer(self, channel, user, end_time, base_name):
        last_name = None
        while True:
            if not await self.channel_exists(channel):
                return

            now = datetime.utcnow()
            remaining = (end_time - now).total_seconds()

            if remaining <= 0:
                await self._delete_channel(channel, user, "expired due to inactivity.")
                return

            voice_state = channel.guild.get_member(user.id)
            if voice_state and voice_state.voice and voice_state.voice.channel == channel:
                try:
                    await channel.edit(name=base_name)
                except:
                    pass
                self.active_channels[channel.id]["joined"] = True
                break

            mins, secs = divmod(int(remaining), 60)
            new_name = f"{base_name} · {mins}m {secs:02d}s left"
            if new_name != last_name:
                try:
                    await channel.edit(name=new_name)
                    last_name = new_name
                except:
                    pass

            await asyncio.sleep(CHECK_INTERVAL)

        asyncio.create_task(self._watch_owner_leave(channel, user, base_name))

    async def _watch_owner_leave(self, channel, user, base_name):
        await asyncio.sleep(5)
        while True:
            if not await self.channel_exists(channel):
                return

            voice_state = channel.guild.get_member(user.id)
            if not voice_state or not voice_state.voice or voice_state.voice.channel != channel:
                end_time = datetime.utcnow() + timedelta(minutes=2)
                last_name = None

                while True:
                    if not await self.channel_exists(channel):
                        return

                    voice_state = channel.guild.get_member(user.id)
                    if voice_state and voice_state.voice and voice_state.voice.channel == channel:
                        try:
                            await channel.edit(name=base_name)
                        except:
                            pass
                        break

                    remaining = (end_time - datetime.utcnow()).total_seconds()
                    if remaining <= 0:
                        await self._delete_channel(channel, user, "expired after you left.")
                        return

                    mins, secs = divmod(int(remaining), 60)
                    new_name = f"{base_name} · {mins}m {secs:02d}s left"
                    if new_name != last_name:
                        try:
                            await channel.edit(name=new_name)
                            last_name = new_name
                        except:
                            pass

                    await asyncio.sleep(CHECK_INTERVAL)

            await asyncio.sleep(5)

    async def _delete_channel(self, channel, user, reason):
        try:
            await channel.delete()
        except:
            return
        self.active_channels.pop(channel.id, None)

        try:
            embed = discord.Embed(
                title="❌ Private Channel Deleted",
                description=f"Your private voice channel was {reason}",
                color=discord.Color.red()
            )
            await user.send(embed=embed)
        except:
            pass

    async def channel_exists(self, channel: discord.VoiceChannel):
        try:
            await channel.guild.fetch_channel(channel.id)
            return True
        except discord.NotFound:
            return False

async def setup(bot):
    await bot.add_cog(PrivateChannel(bot))
