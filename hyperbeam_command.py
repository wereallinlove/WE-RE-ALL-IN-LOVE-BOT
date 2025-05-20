import discord
from discord import app_commands
from discord.ext import commands

VERIFIED_ROLE_ID = 1371885746415341648
ALLOWED_CHANNEL_ID = 1318298515948048549
HYPERBEAM_LINK = "https://hyperbeam.com/v/wereallinlove"
HYPERBEAM_IMAGE_URL = "https://cdn.hyperbeam.com/img/hyperbeam-profile.png"  # replace with your real profile image if different

class HyperbeamCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="hyperbeam", description="Post a watch party link for the server.")
    async def hyperbeam(self, interaction: discord.Interaction):
        # Role check
        if not any(role.id == VERIFIED_ROLE_ID for role in interaction.user.roles):
            return await interaction.response.send_message("You don’t have permission to use this command.", ephemeral=True)

        # Channel check
        if interaction.channel.id != ALLOWED_CHANNEL_ID:
            return await interaction.response.send_message("You can only use this command in the watch party channel.", ephemeral=True)

        # Build the embed
        embed = discord.Embed(
            title=f"🎬 Join {interaction.user.display_name}’s Watch Party",
            description=f"[Click here to join the Hyperbeam session]({HYPERBEAM_LINK})",
            color=0xFF69B4  # pink aesthetic
        )
        embed.set_image(url=HYPERBEAM_IMAGE_URL)

        await interaction.response.send_message(embed=embed, ephemeral=False)

async def setup(bot):
    await bot.add_cog(HyperbeamCommand(bot))
