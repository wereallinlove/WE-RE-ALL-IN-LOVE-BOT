import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime
import pytz

QUOTE_CHANNEL_ID = 1373837923430170684
QUOTE_ROLE_ID = 1373837610249752706
EMBED_COLOR = discord.Color.from_rgb(111, 57, 88)  # #6F3958

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

            guild_id = int(parts[-3])
            channel_id = int(parts[-2])
            message_id = int(parts[-1])

            channel = await self.bot.fetch_channel(channel_id)
            message = await channel.fetch_message(message_id)

            author = message.author
            content = message.content
            timestamp = message.created_at.astimezone(pytz.timezone("America/New_York"))
            formatted_time = timestamp.strftime("%B %d, %Y at %I:%M %p")

            embed = discord.Embed(
                title=f"Quote from {author.display_name}",
                description=content,
                color=EMBED_COLOR
            )
            embed.set_footer(text=f"— (@{author.display_name}), {formatted_time}\nWE'RE ALL IN LOVE {datetime.now().year}")

            if message.attachments:
                for attachment in message.attachments:
                    if attachment.content_type.startswith("image/"):
                        embed.set_image(url=attachment.url)
                        break
                    elif attachment.content_type.startswith("video/"):
                        embed.set_thumbnail(url=attachment.url)
                        break

            quote_channel = self.bot.get_channel(QUOTE_CHANNEL_ID)
            await quote_channel.send(embed=embed)
            await interaction.response.send_message("Quote posted.", ephemeral=True)

        except Exception as e:
            await interaction.response.send_message(f"Error quoting message: {e}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Quote(bot))
