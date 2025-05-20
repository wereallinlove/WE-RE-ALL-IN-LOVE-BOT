# logs.py — Federal Logging System
# Logs EVERYTHING possible to Discord's API
# Log Channel: 1374249689507168337
# Format: Embed with timestamp, profile pic, clear context

import discord
from discord.ext import commands
from discord import app_commands
import datetime
import difflib
import json
import os

LOG_CHANNEL_ID = 1374249689507168337
UPTIME_LOG_PATH = "bot_uptime_log.json"

class Logs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ghost_mentions = {}
        self.log_start_time()

    def log_start_time(self):
        now = datetime.datetime.now().isoformat()
        with open(UPTIME_LOG_PATH, "w") as f:
            json.dump({"last_start": now}, f)

    async def send_log(self, embed: discord.Embed):
        channel = self.bot.get_channel(LOG_CHANNEL_ID)
        if channel:
            await channel.send(embed=embed)
        # Also log to file for redundancy
        with open("logs_output.json", "a") as log_file:
            log_file.write(json.dumps({"title": embed.title, "desc": embed.description, "timestamp": embed.timestamp.isoformat()}) + "\n")

    def format_embed(self, title, description, user=None, color=discord.Color.purple()):
        timestamp = datetime.datetime.now().strftime("%m/%d/%Y at %I:%M %p")
        embed = discord.Embed(title=title, description=description, color=color)
        embed.set_footer(text=f"Logged • {timestamp}")
        if user:
            embed.set_thumbnail(url=user.display_avatar.url)
            embed.set_author(name=f"{user} ({user.id})")
        return embed

    # Bot online
    @commands.Cog.listener()
    async def on_ready(self):
        self.log_start_time()
        embed = self.format_embed("🟢 Bot Started", f"The bot is now online and ready.", color=discord.Color.green())
        await self.send_log(embed)

    # ========== MESSAGE EVENTS ==========
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild and not message.author.bot:
            content = message.content or "*No text*"
            embed = self.format_embed("Message Sent", f"{message.author.mention} in {message.channel.mention}:
{content}", user=message.author)
            if message.attachments:
                embed.add_field(name="Attachments", value="\n".join([a.url for a in message.attachments]), inline=False)
                if message.attachments[0].content_type and message.attachments[0].content_type.startswith("image"):
                    embed.set_image(url=message.attachments[0].url)
            if message.embeds:
                embed.add_field(name="Embedded Content", value=f"Contains {len(message.embeds)} embed(s).", inline=False)
            await self.send_log(embed)
            if message.mentions or message.role_mentions:
                self.ghost_mentions[message.id] = (message.author, message.mentions, message.role_mentions)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.guild and not message.author.bot:
            content = message.content or "*No text*"
            embed = self.format_embed("Message Deleted", f"{message.author.mention} in {message.channel.mention}:
{content}", user=message.author)
            if message.attachments:
                embed.add_field(name="Attachments", value="\n".join([a.url for a in message.attachments]), inline=False)
                if message.attachments[0].content_type and message.attachments[0].content_type.startswith("image"):
                    embed.set_image(url=message.attachments[0].url)
            if message.embeds:
                embed.add_field(name="Embedded Content", value=f"Had {len(message.embeds)} embed(s).", inline=False)
            if message.id in self.ghost_mentions:
                author, mentions, roles = self.ghost_mentions.pop(message.id)
                pinged = ", ".join(m.mention for m in mentions + roles)
                embed.title = "👻 Ghost Ping Detected"
                embed.add_field(name="Pinged", value=pinged or "Unknown", inline=False)
            await self.send_log(embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.guild and not before.author.bot and before.content != after.content:
            diff = '\n'.join(difflib.ndiff(before.content.split(), after.content.split()))
            embed = self.format_embed("Message Edited", f"{before.author.mention} in {before.channel.mention}:
```diff\n{diff}```", user=before.author)
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

    # ========== USER & MEMBER EVENTS ==========
    @commands.Cog.listener()
    async def on_user_update(self, before, after):
        changes = []
        if before.name != after.name:
            changes.append(f"**Username**: {before.name} → {after.name}")
        if before.discriminator != after.discriminator:
            changes.append(f"**Discriminator**: {before.discriminator} → {after.discriminator}")
        if before.avatar != after.avatar:
            changes.append(f"**Avatar Updated**")
        if hasattr(before, 'banner') and hasattr(after, 'banner') and before.banner != after.banner:
            changes.append(f"**Banner Updated**")
        if hasattr(before, 'bio') and hasattr(after, 'bio') and before.bio != after.bio:
            changes.append(f"**Bio Updated**")
        if changes:
            embed = self.format_embed("User Updated", '\n'.join(changes), user=after)
            await self.send_log(embed)

    # ========== PRESENCE ==========
    @commands.Cog.listener()
    async def on_presence_update(self, before, after):
        changes = []
        if before.status != after.status:
            changes.append(f"**Status**: {before.status.name} → {after.status.name}")
        before_activities = {a.name for a in before.activities if a.name}
        after_activities = {a.name for a in after.activities if a.name}
        new = after_activities - before_activities
        ended = before_activities - after_activities
        if new:
            changes.append(f"**Started**: {', '.join(new)}")
        if ended:
            changes.append(f"**Ended**: {', '.join(ended)}")
        if changes:
            embed = self.format_embed("Presence Update", '\n'.join(changes), user=after)
            await self.send_log(embed)

    # ========== VOICE ==========
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        changes = []
        if before.channel != after.channel:
            if before.channel and not after.channel:
                changes.append("**Left Voice Channel**")
            elif after.channel and not before.channel:
                changes.append("**Joined Voice Channel**")
            else:
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
