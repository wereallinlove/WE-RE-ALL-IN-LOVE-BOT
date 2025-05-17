import discord
from discord import app_commands
from discord.ext import commands
import asyncio
import yt_dlp
import random

VOICE_CLIENT = None
QUEUE = []
PLAYLIST_URL = "https://soundcloud.com/your_username/likes"  # <-- Replace with your SoundCloud likes or playlist URL
TEXT_CHANNEL_ID = 1318298515948048549

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def play_next(self, interaction):
        global VOICE_CLIENT
        if not QUEUE:
            await interaction.channel.send("🎵 Playlist finished or empty.")
            return

        track = QUEUE.pop(0)

        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'default_search': 'auto',
            'noplaylist': True,
            'extract_flat': False,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(track, download=False)
            url = info['url']
            title = info.get('title', 'Unknown')
            artist = info.get('uploader', 'Unknown')
            thumbnail = info.get('thumbnail')

        # Play audio
        VOICE_CLIENT.play(discord.FFmpegPCMAudio(url), after=lambda e: asyncio.run_coroutine_threadsafe(self.play_next(interaction), self.bot.loop))

        # Send embed
        embed = discord.Embed(
            title=f"Now Playing: {title}",
            description=f"by **{artist}**",
            color=discord.Color.pink()
        )
        if thumbnail:
            embed.set_thumbnail(url=thumbnail)
        embed.set_footer(text=f"WE'RE ALL IN LOVE {discord.utils.utcnow().year}")

        channel = self.bot.get_channel(TEXT_CHANNEL_ID)
        if channel:
            await channel.send(embed=embed)

    @app_commands.command(name="play", description="Play music from SoundCloud.")
    async def play(self, interaction: discord.Interaction):
        global VOICE_CLIENT

        await interaction.response.defer(ephemeral=True)

        if not interaction.user.voice or not interaction.user.voice.channel:
            await interaction.followup.send("You must be in a voice channel to use this command.")
            return

        voice_channel = interaction.user.voice.channel

        # Connect or move to voice channel
        if interaction.guild.voice_client:
            VOICE_CLIENT = interaction.guild.voice_client
            await VOICE_CLIENT.move_to(voice_channel)
        else:
            VOICE_CLIENT = await voice_channel.connect()

        # Build queue from playlist
        ydl_opts = {
            'quiet': True,
            'extract_flat': True,
            'default_search': 'auto',
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(PLAYLIST_URL, download=False)
            entries = info.get('entries', [])
            links = [entry['url'] for entry in entries]

        random.shuffle(links)
        QUEUE.extend(links)

        await self.play_next(interaction)
        await interaction.followup.send("🎶 Starting playback!", ephemeral=True)

    @app_commands.command(name="stop", description="Stop the music and disconnect.")
    async def stop(self, interaction: discord.Interaction):
        global VOICE_CLIENT, QUEUE
        QUEUE = []

        if interaction.guild.voice_client:
            await interaction.guild.voice_client.disconnect()
            VOICE_CLIENT = None
            await interaction.response.send_message("🛑 Disconnected from voice channel.", ephemeral=True)
        else:
            await interaction.response.send_message("I'm not in a voice channel.", ephemeral=True)

    @app_commands.command(name="shuffle", description="Shuffle the playlist.")
    async def shuffle(self, interaction: discord.Interaction):
        if not QUEUE:
            await interaction.response.send_message("Queue is empty, use /play first.", ephemeral=True)
            return

        random.shuffle(QUEUE)
        await interaction.response.send_message("🔀 Playlist shuffled!", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(Music(bot))
