import discord
from discord.ext import commands
import yt_dlp
import random
import asyncio

QUEUE = []
VC_INSTANCES = {}
TEXT_CHANNEL_ID = 1318298515948048549
MUSIC_ROLE_ID = 1373224259156967465

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def ensure_voice(self, ctx):
        if ctx.author.voice is None:
            await ctx.send("❌ You must be in a voice channel.")
            return None

        voice = ctx.guild.voice_client
        if voice and voice.is_connected():
            return voice

        try:
            voice = await ctx.author.voice.channel.connect()
            VC_INSTANCES[ctx.guild.id] = voice
            return voice
        except discord.ClientException:
            await ctx.send("⚠️ Already connected to a voice channel.")
            return None

    def has_music_role(self, ctx):
        return any(role.id == MUSIC_ROLE_ID for role in ctx.author.roles)

    def get_stream_url(self, query):
        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'noplaylist': True,
            'default_search': 'ytsearch' if not query.startswith("http") else 'auto'
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(query, download=False)
            if 'entries' in info:
                # Take the top result
                info = info['entries'][0]
            return [info['url']], [info]

    async def play_next(self, guild_id):
        voice = VC_INSTANCES.get(guild_id)
        if not voice or not voice.is_connected():
            return

        if not QUEUE:
            await voice.disconnect()
            VC_INSTANCES.pop(guild_id, None)
            return

        url, info = QUEUE.pop(0)

        try:
            source = await discord.FFmpegOpusAudio.from_probe(url, method='fallback')
            voice.play(source, after=lambda e: self.bot.loop.create_task(self.play_next(guild_id)))

            embed = discord.Embed(
                title="🎶 Now Playing",
                description=f"**{info.get('title', 'Unknown')}** by **{info.get('uploader', 'Unknown')}**",
                color=discord.Color.magenta()
            )
            if 'thumbnail' in info:
                embed.set_thumbnail(url=info['thumbnail'])

            channel = self.bot.get_channel(TEXT_CHANNEL_ID)
            if channel:
                await channel.send(embed=embed)
        except Exception as e:
            channel = self.bot.get_channel(TEXT_CHANNEL_ID)
            if channel:
                await channel.send(f"❌ Error loading track: {e}")
            await asyncio.sleep(1)
            await self.play_next(guild_id)

    @commands.command(name="play")
    async def play(self, ctx, *, query: str = None):
        try:
            await ctx.message.delete()
        except:
            pass

        if not self.has_music_role(ctx):
            return
        if not query:
            return

        voice = await self.ensure_voice(ctx)
        if not voice:
            return

        try:
            urls, infos = self.get_stream_url(query)
            if not urls:
                return

            was_playing = voice.is_playing()

            for u, i in zip(urls, infos):
                QUEUE.append((u, i))

            if was_playing:
                embed = discord.Embed(
                    title="➕ Added to Queue",
                    description=f"**{infos[0].get('title', 'Unknown')}** by **{infos[0].get('uploader', 'Unknown')}**",
                    color=discord.Color.magenta()
                )
                if "thumbnail" in infos[0]:
                    embed.set_thumbnail(url=infos[0]["thumbnail"])
                await ctx.send(embed=embed)
            else:
                await asyncio.sleep(1)
                await self.play_next(ctx.guild.id)

        except Exception as e:
            await ctx.send(f"❌ Error: {e}")

    @commands.command(name="skip")
    async def skip(self, ctx):
        try:
            await ctx.message.delete()
        except:
            pass

        if not self.has_music_role(ctx):
            return

        voice = ctx.guild.voice_client
        if voice and voice.is_playing():
            voice.stop()
            await ctx.send("⏭️ Skipped.")
        else:
            await ctx.send("⚠️ Nothing is playing.")

    @commands.command(name="queue")
    async def queue_cmd(self, ctx):
        try:
            await ctx.message.delete()
        except:
            pass

        if not self.has_music_role(ctx):
            return

        if not QUEUE:
            embed = discord.Embed(
                title="📭 Queue is empty.",
                color=discord.Color.magenta()
            )
            await ctx.send(embed=embed)
            return

        embed = discord.Embed(
            title="🎵 Current Queue",
            description="Here’s what’s coming up next:",
            color=discord.Color.magenta()
        )

        for idx, (_, info) in enumerate(QUEUE[:10], start=1):
            title = info.get('title', 'Unknown')
            uploader = info.get('uploader', 'Unknown')
            embed.add_field(
                name=f"{idx}. {title}",
                value=f"by {uploader}",
                inline=False
            )

        await ctx.send(embed=embed)

    @commands.command(name="leave")
    async def leave(self, ctx):
        try:
            await ctx.message.delete()
        except:
            pass

        if not self.has_music_role(ctx):
            return

        voice = ctx.guild.voice_client
        if voice and voice.is_connected():
            await voice.disconnect()
            VC_INSTANCES.pop(ctx.guild.id, None)

            embed = discord.Embed(
                title="👋 Disconnected",
                description="The bot has left the voice channel.",
                color=discord.Color.magenta()
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send("⚠️ I'm not in a voice channel.")

async def setup(bot):
    await bot.add_cog(Music(bot))
