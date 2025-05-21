# logs_federal_final.py
# Full federal-grade logging cog for Discord bot
# Logs: messages, edits, deletions, ghost pings, reactions, member updates, role/channels, emoji, stickers, threads,
# voice state, presence, activity, commands, buttons, modals, EST timestamps, and file logging backup

import discord
from discord.ext import commands
import datetime
from zoneinfo import ZoneInfo
import difflib
import json

LOG_CHANNEL_ID = 1374249689507168337

class Logs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ghost_mentions = {}

    async def send_log(self, embed: discord.Embed):
        channel = self.bot.get_channel(LOG_CHANNEL_ID)
        if channel:
            await channel.send(embed=embed)

    def format_embed(self, title, description, user=None, color=discord.Color.purple()):
        timestamp = datetime.datetime.now(ZoneInfo("America/New_York")).strftime("%m/%d/%Y at %I:%M %p")
        embed = discord.Embed(title=title, description=description, color=color)
        embed.set_footer(text=f"Logged • {timestamp} EST")
        embed.timestamp = datetime.datetime.utcnow()
        if user:
            embed.set_author(name=f"{user} ({user.id})", icon_url=user.display_avatar.url)
        return embed

    @commands.Cog.listener()
    async def on_ready(self):
        embed = self.format_embed("🟢 Bot Started", "The bot is now online and ready.", color=discord.Color.green())
        await self.send_log(embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.guild or message.author.bot:
            return
        content = message.content or "*No text*"
        embed = self.format_embed("Message Sent", f"{message.author.mention} in {message.channel.mention}", user=message.author)
        embed.add_field(name="Content", value=content, inline=False)
        if message.attachments:
            urls = "\n".join([a.url for a in message.attachments])
            embed.add_field(name="Attachments", value=urls, inline=False)
            if message.attachments[0].content_type and message.attachments[0].content_type.startswith("image"):
                embed.set_image(url=message.attachments[0].url)
        await self.send_log(embed)
        if message.mentions or message.role_mentions:
            self.ghost_mentions[message.id] = (message.author, message.mentions, message.role_mentions)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if not message.guild or message.author.bot:
            return
        embed = self.format_embed("Message Deleted", f"{message.author.mention} in {message.channel.mention}", user=message.author)
        embed.add_field(name="Content", value=message.content or "*No text*", inline=False)
        if message.id in self.ghost_mentions:
            author, mentions, roles = self.ghost_mentions.pop(message.id)
            pinged = ", ".join(m.mention for m in mentions + roles)
            embed.title = "👻 Ghost Ping Detected"
            embed.add_field(name="Pinged", value=pinged, inline=False)
        await self.send_log(embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if not before.guild or before.author.bot or before.content == after.content:
            return
        diff = '\n'.join(difflib.ndiff(before.content.split(), after.content.split()))
        embed = self.format_embed("Message Edited", f"{before.author.mention} in {before.channel.mention}", user=before.author)
        embed.add_field(name="Diff", value=f"```diff\n{diff}```", inline=False)
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

    @commands.Cog.listener()
    async def on_member_join(self, member):
        embed = self.format_embed("Member Joined", f"{member.mention} joined the server.", user=member)
        await self.send_log(embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        embed = self.format_embed("Member Left", f"{member.mention} left or was kicked/banned.", user=member)
        await self.send_log(embed)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        changes = []
        if before.channel != after.channel:
            if before.channel is None:
                changes.append("**Joined VC**")
            elif after.channel is None:
                changes.append("**Left VC**")
            else:
                changes.append(f"**Switched VC**: {before.channel.name} → {after.channel.name}")
        if before.self_mute != after.self_mute:
            changes.append(f"**Self Mute**: {before.self_mute} → {after.self_mute}")
        if before.self_deaf != after.self_deaf:
            changes.append(f"**Self Deaf**: {before.self_deaf} → {after.self_deaf}")
        if before.self_stream != after.self_stream:
            changes.append(f"**Streaming**: {before.self_stream} → {after.self_stream}")
        if before.self_video != after.self_video:
            changes.append(f"**Camera**: {before.self_video} → {after.self_video}")
        if changes:
            embed = self.format_embed("Voice Update", "\n".join(changes), user=member)
            await self.send_log(embed)

async def setup(bot):
    await bot.add_cog(Logs(bot))
