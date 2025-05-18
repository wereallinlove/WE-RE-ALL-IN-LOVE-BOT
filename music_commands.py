# music_commands.py — slash command version

import discord
from discord import app_commands
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

    def has_music_role(self, interaction):
        return any(role.id == MUSIC_ROLE_ID for role in interaction.user.roles)

    async def ensure_voice(self, interaction):
        if not interaction.user.voice:
            await interaction.response.send_message(embed=discord.Embed(
                    title="❌ You must be in a voice channel",
                    color=discord.Color.magenta()
                ), ephemeral=True)
            return None

        voice = interaction.guild.voice_client
        if voice and voice.is_connected():
            return voice

        try:
            voice = await interaction.user.voice.channel.connect()
            VC_INSTANCES[interaction.guild.id] = voice
            return voice
        except discord.ClientException:
            await interaction.response.send_message(embed=discord.Embed(
                    title="⚠️ Already connected to a voice channel",
                    color=discord.Color.magenta()
                ), ephemeral=True)
            return None

    def get_stream_url(self, query):
        # Updated to handle playlists properly
        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
                        'default_search': 'auto'
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(query, download=False)
            entries = []
            if 'entries' in info:
                entries = info['entries']
            else:
                entries = [info]
            urls = [entry['url'] for entry in entries if 'url' in entry]
            return urls, entries

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

    @app_commands.command(name="play", description="Play a song or playlist from SoundCloud")
    async def play(self, interaction: discord.Interaction, query: str):
        if not self.has_music_role(interaction):
            return

        voice = await self.ensure_voice(interaction)
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
                await interaction.response.send_message(embed=embed)
            else:
                await interaction.response.send_message(embed=discord.Embed(
                    title="⏳ Loading...",
                    description="Attempting to fetch and play the track...",
                    color=discord.Color.magenta()
                ))
                await asyncio.sleep(1)
                await self.play_next(interaction.guild.id)
        except Exception as e:
            await interaction.response.send_message(f"❌ Error: {e}")

    @app_commands.command(name="skip", description="Skip the current song")
    async def skip(self, interaction: discord.Interaction):
        if not self.has_music_role(interaction):
            return

        voice = interaction.guild.voice_client
        if voice and voice.is_playing():
            voice.stop()
            await interaction.response.send_message("⏭️ Skipped.")
        else:
            await interaction.response.send_message(embed=discord.Embed(
                    title="⚠️ Nothing is playing",
                    color=discord.Color.magenta()
                ))

    @app_commands.command(name="queue", description="Show the current SoundCloud queue")
    async def queue_cmd(self, interaction: discord.Interaction):
        if not self.has_music_role(interaction):
            return

        if not QUEUE:
            embed = discord.Embed(title="📭 Queue is empty.", color=discord.Color.magenta())
            await interaction.response.send_message(embed=embed)
            return

        embed = discord.Embed(
            title="🎵 Current Queue",
            description="Here’s what’s coming up next:",
            color=discord.Color.magenta()
        )

        for idx, (_, info) in enumerate(QUEUE[:10], start=1):
            title = info.get('title', 'Unknown')
            uploader = info.get('uploader', 'Unknown')
            embed.add_field(name=f"{idx}. {title}", value=f"by {uploader}", inline=False)

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="leave", description="Disconnect the bot from voice")
    async def leave(self, interaction: discord.Interaction):
        if not self.has_music_role(interaction):
            return

        voice = interaction.guild.voice_client
        if voice and voice.is_connected():
            await voice.disconnect()
            VC_INSTANCES.pop(interaction.guild.id, None)
            embed = discord.Embed(
                title="👋 Disconnected",
                description="The bot has left the voice channel.",
                color=discord.Color.magenta()
            )
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("⚠️ I'm not in a voice channel.")

    @app_commands.command(name="shuffle", description="Shuffle the current SoundCloud queue")
    async def shuffle(self, interaction: discord.Interaction):
        if not self.has_music_role(interaction):
            return

        if len(QUEUE) < 2:
            embed = discord.Embed(title="ℹ️ Not enough tracks to shuffle.", color=discord.Color.magenta())
            await interaction.response.send_message(embed=embed)
            return

        random.shuffle(QUEUE)
        embed = discord.Embed(title="🔀 Queue Shuffled", description="The current queue has been shuffled.", color=discord.Color.magenta())
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Music(bot))