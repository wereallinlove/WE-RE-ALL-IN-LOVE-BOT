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

    @app_commands.command(name="pin", description="Post an image (PNG, JPG, or WEBP only) to the pins channel.")
    @app_commands.describe(
        link="(Required) Direct link to a PNG, JPG, or WEBP image.",
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
        if PIN_ROLE_ID not in [role.id for role in interaction.user.roles]:
            await interaction.response.send_message("You don't have permission to use this command.", ephemeral=True)
            return

        valid_extensions = (".png", ".jpg", ".jpeg", ".webp")
        if not any(link.lower().endswith(ext) for ext in valid_extensions):
            await interaction.response.send_message("❌ Only direct image links ending in .png, .jpg, .jpeg, or .webp are allowed. No GIFs or videos.", ephemeral=True)
            return

        await interaction.response.defer(ephemeral=True)

        current_year = datetime.now().year
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
        embed.set_footer(text=f"WE'RE ALL IN LOVE {current_year}")

        channel = interaction.guild.get_channel(PIN_CHANNEL_ID)
        if not channel:
            await interaction.followup.send("Couldn't find the pin channel.", ephemeral=True)
            return

        await channel.send(embed=embed)
        await interaction.followup.send("Your image was pinned. 📌", ephemeral=True)

async def setup(bot):
    await bot.add_cog(PinCommand(bot))
