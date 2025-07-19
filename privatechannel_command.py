# privatechannel_command.py

import discord
from discord.ext import commands
from discord import app_commands
import asyncio
from datetime import datetime, timedelta

PRIVATE_ROLE_ID = 1396039656004653107
MEMBER_ROLE_ID = 1371885746415341648
CATEGORY_ID = 1395539999537238106

class PrivateChannel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_channels = {}  # {channel_id: owner_id}

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

        # Start initial 2-minute join timer
        asyncio.create_task(self._initial_join_timer(channel, user))

    async def _initial_join_timer(self, channel, user):
        await asyncio.sleep(120)

        if not await self.channel_exists(channel):
            return

        # Check if owner joined
        member = channel.guild.get_member(user.id)
        if not member or not member.voice or member.voice.channel != channel:
            try:
                await channel.delete()
            except:
                pass

            self.active_channels.pop(channel.id, None)

            try:
                embed = discord.Embed(
                    title="❌ Private Channel Deleted",
                    description="Your private voice channel was deleted because you didn’t join within 2 minutes.",
                    color=discord.Color.red()
                )
                await user.send(embed=embed)
            except:
                pass
            return

        # Owner joined — start empty channel watcher
        asyncio.create_task(self._watch_channel_empty(channel, user))

    async def _watch_channel_empty(self, channel, user):
        while await self.channel_exists(channel):
            await asyncio.sleep(5)

            # Check if channel is now empty
            if len(channel.members) == 0:
                # Start deletion timer for inactivity
                delete_at = datetime.utcnow() + timedelta(minutes=2)

                while datetime.utcnow() < delete_at:
                    if not await self.channel_exists(channel):
                        return

                    if len(channel.members) > 0:
                        # Someone rejoined, cancel deletion
                        break
                    await asyncio.sleep(5)

                # Check again after 2 minutes
                if len(channel.members) == 0 and await self.channel_exists(channel):
                    try:
                        await channel.delete()
                    except:
                        pass

                    self.active_channels.pop(channel.id, None)

                    try:
                        embed = discord.Embed(
                            title="❌ Private Channel Deleted",
                            description="Your private voice channel was deleted because everyone left and it was inactive.",
                            color=discord.Color.red()
                        )
                        await user.send(embed=embed)
                    except:
                        pass
                    return

    async def channel_exists(self, channel: discord.VoiceChannel):
        try:
            await channel.guild.fetch_channel(channel.id)
            return True
        except discord.NotFound:
            return False

async def setup(bot):
    await bot.add_cog(PrivateChannel(bot))
