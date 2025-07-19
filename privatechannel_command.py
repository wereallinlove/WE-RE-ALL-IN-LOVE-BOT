# privatechannel_command.py

import discord
from discord import app_commands
from discord.ext import commands
import asyncio
from datetime import datetime, timedelta

PRIVATE_ROLE_ID = 1396039656004653107
MEMBER_ROLE_ID = 1371885746415341648
MOVE_ROLE_ID = 1387282787773710376
CATEGORY_ID = 1395539999537238106

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

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            guild.get_role(MEMBER_ROLE_ID): discord.PermissionOverwrite(view_channel=True, connect=False),
            user: discord.PermissionOverwrite(view_channel=True, connect=True, manage_channels=True, move_members=True),
        }

        channel = await guild.create_voice_channel(
            name=base_name,
            overwrites=overwrites,
            category=category
        )

        end_time = datetime.utcnow() + timedelta(minutes=2)
        self.active_channels[channel.id] = {"owner": user.id, "timeout": end_time, "joined": False}

        await interaction.response.send_message(
            f"✅ Created your private channel: {channel.mention}\n⚠️ You have 2 minutes to join or it will be deleted for inactivity.",
            ephemeral=True
        )

        asyncio.create_task(self._watch_initial_join(channel, user, end_time))

    async def _watch_initial_join(self, channel, user, end_time):
        while True:
            if not await self.channel_exists(channel):
                return

            now = datetime.utcnow()
            if now >= end_time:
                await self._delete_channel(channel, user, "expired due to inactivity.")
                return

            voice_state = channel.guild.get_member(user.id)
            if voice_state and voice_state.voice and voice_state.voice.channel == channel:
                self.active_channels[channel.id]["joined"] = True
                await self._grant_move_role(user)
                asyncio.create_task(self._watch_owner_leave(channel, user))
                return

            await asyncio.sleep(5)

    async def _watch_owner_leave(self, channel, user):
        while True:
            if not await self.channel_exists(channel):
                return

            voice_state = channel.guild.get_member(user.id)
            if not voice_state or not voice_state.voice or voice_state.voice.channel != channel:
                await self._remove_move_role(user)

                # Start countdown to delete
                end_time = datetime.utcnow() + timedelta(minutes=2)
                while True:
                    if not await self.channel_exists(channel):
                        return

                    voice_state = channel.guild.get_member(user.id)
                    if voice_state and voice_state.voice and voice_state.voice.channel == channel:
                        await self._grant_move_role(user)
                        break

                    if datetime.utcnow() >= end_time:
                        await self._delete_channel(channel, user, "expired after you left.")
                        return

                    await asyncio.sleep(5)

            await asyncio.sleep(5)

    async def _grant_move_role(self, user):
        try:
            role = user.guild.get_role(MOVE_ROLE_ID)
            if role and role not in user.roles:
                await user.add_roles(role)
        except:
            pass

    async def _remove_move_role(self, user):
        try:
            role = user.guild.get_role(MOVE_ROLE_ID)
            if role and role in user.roles:
                await user.remove_roles(role)
        except:
            pass

    async def _delete_channel(self, channel, user, reason):
        try:
            await channel.delete()
        except:
            return
        self.active_channels.pop(channel.id, None)
        await self._remove_move_role(user)

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
