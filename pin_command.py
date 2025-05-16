import discord
from discord import app_commands
from datetime import datetime
from typing import Optional

PIN_CHANNEL_ID = 1372918174877614100
PIN_ROLE_ID = 1372919338776133723

def setup(bot):
    @bot.tree.command(name="pin", description="Post a memory (image or video) to the pins channel.")
    @app_commands.describe(
        caption="Optional caption for the memory",
        members="Tag any members who are in the clip or picture"
    )
    async def pin(
        interaction: discord.Interaction,
        caption: Optional[str] = None,
        members: Optional[str] = None
    ):
        if PIN_ROLE_ID not in [role.id for role in interaction.user.roles]:
            await interaction.response.send_message("You don't have permission to use this command.", ephemeral=True)
            return

        if not interaction.attachments:
            await interaction.response.send_message("You must attach an image or video to pin.", ephemeral=True)
            return

        file = interaction.attachments[0]
        current_year = datetime.now().year

        embed = discord.Embed(
            title="New Pin",
            color=discord.Color.from_rgb(255, 100, 180)
        )

        if caption:
            embed.description = f"*{caption}*"

        embed.set_image(url=file.url)
        embed.add_field(name="Submitted by", value=interaction.user.mention, inline=False)

        if members:
            embed.add_field(name="Featuring", value=members, inline=False)

        embed.set_footer(text=f"WE'RE ALL IN LOVE {current_year}")

        channel = bot.get_channel(PIN_CHANNEL_ID)
        if channel:
            await channel.send(embed=embed)
            await interaction.response.send_message("Your memory was pinned. 📌", ephemeral=True)
        else:
            await interaction.response.send_message("Couldn't find the pin channel.", ephemeral=True)
