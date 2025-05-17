
import discord
from discord import app_commands
from datetime import datetime
from typing import Optional

PIN_CHANNEL_ID = 1372918174877614100
PIN_ROLE_ID = 1372919338776133723

class PinCommand(discord.ext.commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="pin", description="Post an image or gif to the pins channel.")
    @app_commands.describe(
        link="Paste a direct image link (.jpg, .png, .gif, etc.)",
        caption="Optional caption for the memory",
        members="Tag any members who are in the image"
    )
    async def pin(
        self,
        interaction: discord.Interaction,
        link: Optional[str],
        caption: Optional[str] = None,
        members: Optional[str] = None
    ):
        if PIN_ROLE_ID not in [role.id for role in interaction.user.roles]:
            await interaction.response.send_message("You don't have permission to use this command.", ephemeral=True)
            return

        await interaction.response.defer(ephemeral=True)

        image_url = None

        if link and (link.lower().endswith((".jpg", ".jpeg", ".png", ".gif", ".webp")) or "cdn.discordapp.com" in link):
            image_url = link
        else:
            # fallback: look for recent attachment if no valid link
            history = [
                msg async for msg in interaction.channel.history(limit=5)
                if msg.author.id == interaction.user.id and msg.attachments
            ]
            if history:
                file = history[0].attachments[0]
                if file.content_type and file.content_type.startswith("image"):
                    image_url = file.url

        if not image_url:
            await interaction.followup.send("You must provide a valid image link (jpg, png, gif) or attach an image.", ephemeral=True)
            return

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

        embed.set_footer(text=f"WE'RE ALL IN LOVE {current_year}")
        embed.set_image(url=image_url)

        channel = interaction.guild.get_channel(PIN_CHANNEL_ID)
        if not channel:
            await interaction.followup.send("Couldn't find the pin channel.", ephemeral=True)
            return

        await channel.send(embed=embed)
        await interaction.followup.send("Your image was pinned. 📌", ephemeral=True)

async def setup(bot):
    await bot.add_cog(PinCommand(bot))
