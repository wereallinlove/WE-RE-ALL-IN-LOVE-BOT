# privatechannel_command.py

import discord
from discord.ext import commands
from discord import app_commands
import asyncio
from datetime import datetime, timedelta

PRIVATE_ROLE_ID = 1396039656004653107
MEMBER_ROLE_ID = 1371885746415341648
MOVE_ROLE_ID = 1387282787773710376
CATEGORY_ID = 1395539999537238106

class PrivateChannel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_channels = {}  # channel_id: owner_id

    @app_commands.command(name="privatechannel", description="Create your own private voice channel.")
    @app_commands.checks.has_role(PRIVATE_ROLE_ID)
    async def privatechannel(self, interaction: discord.Interaction):
        user = interaction.user
        guild = interaction.guild
        category = guild.get_channel(CATEGORY_ID)

        channel_name = f"{user.display_name} · @{user.name}'s channel"
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            guild.get_role(MEMBER_ROLE_ID): discord.PermissionOverwrite(view_channel=True, connect=False),
            user: discord.PermissionOverwrite(view_channel=True, connect=True, manage_channels=True, move_members=True),
        }

        # Create the private voice channel
        channel = await guild.create_voice_channel(
            name=channel_name,
            overwrites=overwrites,
            category=category
        )

        self.active_channels[channel.id] = user.id

        await interaction.response.send_message(
            f"✅ Created your private channel: {channel.mention}\n⚠️ You have 2 minutes to join or it will be deleted for inactivity.",
            ephemeral=True
        )

        # Start deletion timer if user doesn't join
        await self._start_inactivity_timer(channel, user)

    async def _start_inactivity_timer(self, channel, user):
        await asyncio.sleep(120)

        # If the channel still exists and user hasn’t joined, delete it
        voice_state = user.voice
        if voice_state is None or voice_state.channel != channel:
            try:
                await channel.delete()
                await self._remove_move_role(user)
            except:
                pass

            try:
                embed = discord.Embed(
                    title="❌ Private Channel Deleted",
                    description="Your private voice channel was deleted because you didn’t join within 2 minutes.",
                    color=discord.Color.red()
                )
                await user.send(embed=embed)
            except:
                pass

            self.active_channels.pop(channel.id, None)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        # Check if the user is the owner of one of the tracked private channels
        move_role = member.guild.get_role(MOVE_ROLE_ID)

        # User joined a channel
        if after.channel and after.channel.id in self.active_channels:
            owner_id = self.active_channels.get(after.channel.id)
            if member.id == owner_id:
                if move_role and move_role not in member.roles:
                    try:
                        await member.add_roles(move_role)
                    except:
                        pass

        # User left a channel
        if before.channel and before.channel.id in self.active_channels:
            owner_id = self.active_channels.get(before.channel.id)
            if member.id == owner_id:
                if move_role and move_role in member.roles:
                    try:
                        await member.remove_roles(move_role)
                    except:
                        pass

    async def _remove_move_role(self, user):
        try:
            role = user.guild.get_role(MOVE_ROLE_ID)
            if role and role in user.roles:
                await user.remove_roles(role)
        except:
            pass

async def setup(bot):
    await bot.add_cog(PrivateChannel(bot))
