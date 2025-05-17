import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import yt_dlp

QUEUE = []
VC_INSTANCES = {}  # guild_id: voice_client
TEXT_CHANNEL_ID = 1318298515948048549

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def ensure_voice(self, interaction: discord.Interaction):
        if interaction.user.voice is None:
            await interaction.response.send_message("❌ You must be in a voice channel.", ephemeral=True)
            return None
        voice = VC_INSTANCES.get(interaction.guild.id)
        if not voice or not voice.is_connected():
            VC_INSTANCES[interaction.guild.id] = await interaction.user.voice.channel.connect()
        return VC_INSTANCES[interaction.guild.id]

    def get_stream_url(self, url):
        ydl_opts = {
            'format': 'bestaudio/best',
            'noplaylist': False,
            'quiet': True,
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
        voice.play(source, after=lambda e: asyncio.run_coroutine_threadsafe(self.play_next(guild_id), self.bot.loop))

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

    @app_commands.command(name="play2", description="Play a SoundCloud link, playlist, or likes.")
    @app_commands.describe(url="SoundCloud track, playlist, or likes link")
    async def play2(self, interaction: discord.Interaction, url: str):
        voice = await self.ensure_voice(interaction)
        if not voice:
            return

        await interaction.response.send_message("🔍 Loading...", ephemeral=True)

        try:
            urls, infos = self.get_stream_url(url)
            for u, i in zip(urls, infos):
                QUEUE.append((u, i))

            await interaction.followup.send(f"✅ Added {len(urls)} track(s) to the queue.", ephemeral=True)

            if not voice.is_playing():
                await self.play_next(interaction.guild.id)
        except Exception as e:
            await interaction.followup.send(f"❌ Failed to load: {e}", ephemeral=True)

    @app_commands.command(name="skip", description="Skip the current track.")
    async def skip(self, interaction: discord.Interaction):
        voice = VC_INSTANCES.get(interaction.guild.id)
        if voice and voice.is_playing():
            voice.stop()
            await interaction.response.send_message("⏭️ Skipped.", ephemeral=False)
        else:
            await interaction.response.send_message("⚠️ Nothing is playing.", ephemeral=True)

    @app_commands.command(name="queue", description="See what songs are in the queue.")
    async def queue(self, interaction: discord.Interaction):
        if not QUEUE:
            await interaction.response.send_message("📭 Queue is empty.", ephemeral=False)
            return

        embed = discord.Embed(title="🎶 Queue", color=discord.Color.blurple())
        for idx, (_, info) in enumerate(QUEUE[:10]):
            embed.add_field(name=f"{idx+1}.", value=f"{info.get('title', 'Unknown')} - {info.get('uploader', 'Unknown')}", inline=False)
        await interaction.response.send_message(embed=embed, ephemeral=False)

async def setup(bot: commands.Bot):
    await bot.add_cog(Music(bot))
