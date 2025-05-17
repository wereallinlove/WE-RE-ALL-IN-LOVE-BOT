import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime
from typing import Optional

PIN_CHANNEL_ID = 1372918174877614100
PIN_ROLE_ID = 1372919338776133723

class PinCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="pin",
        description="Post a direct image link to the pins channel (PNG, JPG, GIF, WEBP, etc.)."
    )
    @app_commands.describe(
        link="(Required) Direct link to an image (GIFs allowed).",
        caption="Optional caption for the memory",
        members="Optional: Tag members who are in the image"
    )
    async def pin(
        self,
        interaction: discord.Interaction,
        link: str,
        caption: Optional[str] = None,
        members: Optional[str] = None
    ):
        # permission check
        if PIN_ROLE_ID not in [role.id for role in interaction.user.roles]:
            await interaction.response.send_message(
                "You don't have permission to use this command.",
                ephemeral=True
            )
            return

        # block common video links
        lower = link.lower()
        if lower.endswith((".mp4", ".mov", ".webm")):
            await interaction.response.send_message(
                "❌ Videos are not allowed. Please provide an image link (PNG, JPG, GIF, WEBP, etc.).",
                ephemeral=True
            )
            return

        # defer so we can build/embed
        await interaction.response.defer(ephemeral=True)

        now_year = datetime.now().year
        embed = discord.Embed(
            title="New Pin 📌",
            color=discord.Color.from_rgb(255, 100, 180)
        )
        if caption:
            embed.description = f"*{caption}*"

        embed.add_field(name="Submitted by", value=interaction.user.mention, inline=False)
        if members:
            embed.add_field(name="Featuring", value=members, inline=False)

        embed.set_image(url=link)
        embed.set_footer(text=f"WE'RE ALL IN LOVE {now_year}")

        # send to your pins channel
        channel = interaction.guild.get_channel(PIN_CHANNEL_ID)
        if not channel:
            await interaction.followup.send(
                "Couldn't find the pin channel. Please check configuration.",
                ephemeral=True
            )
            return

        await channel.send(embed=embed)
        await interaction.followup.send("Your image was pinned. 📌", ephemeral=True)

async def setup(bot):
    await bot.add_cog(PinCommand(bot))
