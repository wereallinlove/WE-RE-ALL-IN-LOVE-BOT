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

    def get_stream_url(self, url):
        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'extract_flat': False,
            'default_search': 'auto',
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            if 'entries' in info:
                entries = [e for e in info['entries'] if 'url' in e]
                random.shuffle(entries)
                return [entry['url'] for entry in entries], entries
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
    async def play(self, ctx, *, url: str = None):
        await ctx.message.delete()

        if not self.has_music_role(ctx):
            return
        if not url:
            return

        voice = await self.ensure_voice(ctx)
        if not voice:
            return

        try:
            urls, infos = self.get_stream_url(url)
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
        await ctx.message.delete()

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
        await ctx.message.delete()

        if not self.has_music_role(ctx):
            return

        if not QUEUE:
            await ctx.send("📭 Queue is empty.")
            return
        msg = "**📜 Current Queue:**\n"
        for idx, (_, info) in enumerate(QUEUE[:10]):
            title = info.get('title', 'Unknown')
            uploader = info.get('uploader', 'Unknown')
            msg += f"{idx + 1}. {title} — {uploader}\n"
        await ctx.send(msg)

    @commands.command(name="leave")
    async def leave(self, ctx):
        await ctx.message.delete()

        if not self.has_music_role(ctx):
            return

        voice = ctx.guild.voice_client
        if voice and voice.is_connected():
            await voice.disconnect()
            VC_INSTANCES.pop(ctx.guild.id, None)
            await ctx.send("👋 Left the voice channel.")
        else:
            await ctx.send("⚠️ I'm not in a voice channel.")

async def setup(bot):
    await bot.add_cog(Music(bot))
