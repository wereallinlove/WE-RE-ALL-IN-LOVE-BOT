import discord
from discord.ext import commands
import yt_dlp

QUEUE = []
VC_INSTANCES = {}  # guild_id: voice client
TEXT_CHANNEL_ID = 1318298515948048549

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def ensure_voice(self, ctx):
        if ctx.author.voice is None:
            await ctx.send("❌ You must be in a voice channel.")
            return None
        voice = VC_INSTANCES.get(ctx.guild.id)
        if not voice or not voice.is_connected():
            VC_INSTANCES[ctx.guild.id] = await ctx.author.voice.channel.connect()
        return VC_INSTANCES[ctx.guild.id]

    def get_stream_url(self, url):
        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'noplaylist': False,
            'extract_flat': False,
            'default_search': 'auto',
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            if 'entries' in info:
                return [entry['url'] for entry in info['entries']], info['entries']
            return [info['url']], [info]

    async def play_next(self, guild_id):
        if not QUEUE:
            await VC_INSTANCES[guild_id].disconnect()
            del VC_INSTANCES[guild_id]
            return

        url, info = QUEUE.pop(0)
        voice = VC_INSTANCES[guild_id]
        source = await discord.FFmpegOpusAudio.from_probe(url, method='fallback')
        voice.play(source, after=lambda e: self.bot.loop.create_task(self.play_next(guild_id)))

        embed = discord.Embed(
            title="🎵 Now Playing",
            description=f"**{info.get('title', 'Unknown')}** by **{info.get('uploader', 'Unknown')}**",
            color=discord.Color.purple()
        )
        if 'thumbnail' in info:
            embed.set_thumbnail(url=info['thumbnail'])

        channel = self.bot.get_channel(TEXT_CHANNEL_ID)
        if channel:
            await channel.send(embed=embed)

    @commands.command(name="play")
    async def play(self, ctx, *, url: str):
        voice = await self.ensure_voice(ctx)
        if not voice:
            return
        await ctx.send("🔍 Loading...")

        try:
            urls, infos = self.get_stream_url(url)
            for u, i in zip(urls, infos):
                QUEUE.append((u, i))
            await ctx.send(f"✅ Added {len(urls)} track(s) to the queue.")
            if not voice.is_playing():
                await self.play_next(ctx.guild.id)
        except Exception as e:
            await ctx.send(f"❌ Error: {e}")

    @commands.command(name="skip")
    async def skip(self, ctx):
        voice = VC_INSTANCES.get(ctx.guild.id)
        if voice and voice.is_playing():
            voice.stop()
            await ctx.send("⏭️ Skipped.")
        else:
            await ctx.send("⚠️ Nothing is playing.")

    @commands.command(name="queue")
    async def queue_cmd(self, ctx):
        if not QUEUE:
            await ctx.send("📭 Queue is empty.")
            return
        msg = "**Queue:**\n"
        for idx, (_, info) in enumerate(QUEUE[:10]):
            msg += f"{idx + 1}. {info.get('title', 'Unknown')} - {info.get('uploader', 'Unknown')}\n"
        await ctx.send(msg)

async def setup(bot):
    await bot.add_cog(Music(bot))
