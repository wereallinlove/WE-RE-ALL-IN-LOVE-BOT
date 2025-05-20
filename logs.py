# logs.py — COMPLETE FEDERAL LOGGING SYSTEM
# Channel ID: 1374249689507168337

import discord
from discord.ext import commands
from discord import app_commands
import datetime
import difflib

LOG_CHANNEL_ID = 1374249689507168337

class Logs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def send_log(self, embed: discord.Embed):
        channel = self.bot.get_channel(LOG_CHANNEL_ID)
        if channel:
            await channel.send(embed=embed)

    def format_embed(self, title, description, user=None, color=discord.Color.purple()):
        embed = discord.Embed(title=title, description=description, color=color)
        embed.timestamp = datetime.datetime.utcnow()
        if user:
            embed.set_thumbnail(url=user.display_avatar.url)
            embed.set_author(name=f"{user} ({user.id})")
        return embed

    # ========== MESSAGE EVENTS ==========

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild and not message.author.bot:
            embed = self.format_embed("Message Sent", f"{message.author.mention} in {message.channel.mention}:\n{message.content}", user=message.author)
            await self.send_log(embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.guild and not before.author.bot and before.content != after.content:
            diff = '\n'.join(difflib.ndiff(before.content.split(), after.content.split()))
            embed = self.format_embed("Message Edited", f"{before.author.mention} in {before.channel.mention}:\n```diff\n{diff}```", user=before.author)
            await self.send_log(embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.guild and not message.author.bot:
            embed = self.format_embed("Message Deleted", f"{message.author.mention} in {message.channel.mention}:\n{message.content}", user=message.author)
            await self.send_log(embed)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if reaction.message.guild and not user.bot:
            embed = self.format_embed("Reaction Added", f"{user.mention} reacted with {reaction.emoji} in {reaction.message.channel.mention}", user=user)
            await self.send_log(embed)

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        if reaction.message.guild and not user.bot:
            embed = self.format_embed("Reaction Removed", f"{user.mention} removed {reaction.emoji} in {reaction.message.channel.mention}", user=user)
            await self.send_log(embed)

    # ========== MEMBER EVENTS ==========

    @commands.Cog.listener()
    async def on_member_join(self, member):
        embed = self.format_embed("Member Joined", f"{member.mention} has joined the server.", user=member)
        await self.send_log(embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        embed = self.format_embed("Member Left", f"{member.mention} has left the server.", user=member)
        await self.send_log(embed)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        changes = []
        if before.nick != after.nick:
            changes.append(f"**Nickname**: {before.nick} → {after.nick}")
        if before.roles != after.roles:
            before_roles = set(before.roles)
            after_roles = set(after.roles)
            added = after_roles - before_roles
            removed = before_roles - after_roles
            if added:
                changes.append(f"**Roles Added**: {', '.join(role.name for role in added)}")
            if removed:
                changes.append(f"**Roles Removed**: {', '.join(role.name for role in removed)}")
        if before.timed_out_until != after.timed_out_until:
            changes.append(f"**Timeout**: {before.timed_out_until} → {after.timed_out_until}")
        if changes:
            embed = self.format_embed("Member Updated", '\n'.join(changes), user=after)
            await self.send_log(embed)

    @commands.Cog.listener()
    async def on_user_update(self, before, after):
        changes = []
        if before.name != after.name:
            changes.append(f"**Username**: {before.name} → {after.name}")
        if before.discriminator != after.discriminator:
            changes.append(f"**Discriminator**: {before.discriminator} → {after.discriminator}")
        if before.avatar != after.avatar:
            changes.append("**Avatar Updated**")
        if changes:
            embed = self.format_embed("User Updated", '\n'.join(changes), user=after)
            await self.send_log(embed)

    # ========== PRESENCE EVENTS ==========

    @commands.Cog.listener()
    async def on_presence_update(self, before, after):
        if before.status != after.status:
            embed = self.format_embed("Status Changed", f"{before.name} is now **{after.status.name.upper()}**", user=after)
            await self.send_log(embed)

    # ========== VOICE EVENTS ==========

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        changes = []
        if before.channel != after.channel:
            if before.channel and not after.channel:
                changes.append("**Left Voice Channel**")
            elif after.channel and not before.channel:
                changes.append("**Joined Voice Channel**")
            elif before.channel != after.channel:
                changes.append(f"**Switched Channel**: {before.channel.name} → {after.channel.name}")
        if before.self_mute != after.self_mute:
            changes.append(f"**Self Mute**: {before.self_mute} → {after.self_mute}")
        if before.self_deaf != after.self_deaf:
            changes.append(f"**Self Deaf**: {before.self_deaf} → {after.self_deaf}")
        if before.mute != after.mute:
            changes.append(f"**Server Mute**: {before.mute} → {after.mute}")
        if before.deaf != after.deaf:
            changes.append(f"**Server Deaf**: {before.deaf} → {after.deaf}")
        if before.self_stream != after.self_stream:
            changes.append(f"**Streaming**: {before.self_stream} → {after.self_stream}")
        if before.self_video != after.self_video:
            changes.append(f"**Camera**: {before.self_video} → {after.self_video}")
        if changes:
            embed = self.format_embed("Voice Update", '\n'.join(changes), user=member)
            await self.send_log(embed)

async def setup(bot):
    await bot.add_cog(Logs(bot))
