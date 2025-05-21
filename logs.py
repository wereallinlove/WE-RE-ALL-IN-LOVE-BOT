
import discord
from discord.ext import commands
import datetime
import difflib
import json

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

    def format_embed(self, title, description, user=None, color=discord.Color.purple()):
        timestamp = datetime.datetime.now().strftime("%m/%d/%Y at %I:%M %p")
        embed = discord.Embed(title=title, description=description, color=color)
        embed.set_footer(text=f"Logged • {timestamp}")
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
        await self.send_log(embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if not message.guild or message.author.bot:
            return
        embed = self.format_embed("Message Deleted", f"{message.author.mention} in {message.channel.mention}", user=message.author)
        content = message.content or "*No text*"
        embed.add_field(name="Content", value=content, inline=False)
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
    async def on_member_join(self, member):
        embed = self.format_embed("Member Joined", f"{member.mention} has joined the server.", user=member)
        await self.send_log(embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        embed = self.format_embed("Member Left", f"{member.mention} has left or was removed from the server.", user=member)
        await self.send_log(embed)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        changes = []
        if before.channel != after.channel:
            if before.channel is None:
                changes.append("**Joined Voice Channel**")
            elif after.channel is None:
                changes.append("**Left Voice Channel**")
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
            embed = self.format_embed("Voice Update", "\n".join(changes), user=member)
            await self.send_log(embed)

async def setup(bot):
    await bot.add_cog(Logs(bot))
