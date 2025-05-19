import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime, timezone, timedelta

QUOTE_CHANNEL_ID = 1373837923430170684
QUOTE_ROLE_ID = 1373837610249752706
EMBED_COLOR = discord.Color.from_rgb(231, 84, 128)  # #E75480

class Quote(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="quote", description="Quote a message by link.")
    @app_commands.checks.has_role(QUOTE_ROLE_ID)
    async def quote(self, interaction: discord.Interaction, message_link: str):
        try:
            parts = message_link.strip().split("/")
            if len(parts) < 3:
                raise ValueError("Invalid link format.")

            channel_id = int(parts[-2])
            message_id = int(parts[-1])

            channel = await self.bot.fetch_channel(channel_id)
            message = await channel.fetch_message(message_id)

            author = message.author
            content = message.content

            # Convert to EST
            est_time = message.created_at.replace(tzinfo=timezone.utc).astimezone(timezone(timedelta(hours=-4)))
            formatted_time = est_time.strftime("%B %d, %Y at %I:%M %p")

            # Build embed
            embed = discord.Embed(
                title=f"Quote from {author.display_name}",
                description=content,
                color=EMBED_COLOR
            )
            embed.set_thumbnail(url=author.display_avatar.url)

            # Actual mention in embed body
            embed.add_field(
                name="",
                value=f"— {author.mention}, {formatted_time}",
                inline=False
            )

            quote_channel = self.bot.get_channel(QUOTE_CHANNEL_ID)
            await quote_channel.send(embed=embed)
            await interaction.response.send_message("Quote posted.", ephemeral=True)

        except Exception as e:
            await interaction.response.send_message(f"Error quoting message: {e}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Quote(bot))
