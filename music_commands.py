@app_commands.command(name="play", description="Play a song from YouTube or SoundCloud")
async def play(self, interaction: discord.Interaction, query: str):
    if not self.has_music_role(interaction):
        return

    voice = await self.ensure_voice(interaction)
    if not voice:
        return

    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'noplaylist': True,
            'default_search': 'auto'
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(query, download=False)
            if 'entries' in info:
                info = info['entries'][0]
            url = info['url']

        was_playing = voice.is_playing()
        QUEUE.append((url, info))

        if was_playing:
            embed = discord.Embed(
                title="➕ Added to Queue",
                description=f"**{info.get('title', 'Unknown')}** by **{info.get('uploader', 'Unknown')}**",
                color=discord.Color.magenta()
            )
            if 'thumbnail' in info:
                embed.set_thumbnail(url=info['thumbnail'])
            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(
                title="⏳ Loading...",
                description="Attempting to fetch and play the track...",
                color=discord.Color.magenta()
            )
            await interaction.response.send_message(embed=embed)
            await asyncio.sleep(1)
            await self.play_next(interaction.guild.id)

    except Exception as e:
        await interaction.response.send_message(f"❌ Error: {e}")
