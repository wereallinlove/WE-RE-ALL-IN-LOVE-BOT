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
        with open("logs_output.json", "a") as log_file:
            log_file.write(json.dumps({
                "title": embed.title,
                "desc": embed.description,
                "timestamp": embed.timestamp.isoformat()
            }) + "\n")

    def format_embed(self, title, description, user=None, color=discord.Color.purple()):
        timestamp = datetime.datetime.now().strftime("%m/%d/%Y at %I:%M %p")
        embed = discord.Embed(title=title, description=description, color=color)
        embed.set_footer(text=f"Logged • {timestamp}")
        embed.timestamp = datetime.datetime.utcnow()
        if user:
            embed.set_thumbnail(url=user.display_avatar.url)
            embed.set_author(name=f"{user} ({user.id})")
        return embed

    @commands.Cog.listener()
    async def on_ready(self):
        self.log_start_time()
        embed = self.format_embed("🟢 Bot Started", "The bot is now online and ready.", color=discord.Color.green())
        await self.send_log(embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild and not message.author.bot:
            content = message.content or "*No text*"
            embed = self.format_embed("Message Sent", f"{message.author.mention} in {message.channel.mention}:", user=message.author)
            embed.add_field(name="Content", value=content, inline=False)
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
            embed = self.format_embed("Message Deleted", f"{message.author.mention} in {message.channel.mention}:", user=message.author)
            embed.add_field(name="Content", value=content, inline=False)
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
            embed = self.format_embed("Message Edited", f"{before.author.mention} in {before.channel.mention}:", user=before.author)
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

async def setup(bot):
    await bot.add_cog(Logs(bot))
