import discord
from discord import app_commands
from discord.ext import commands

VERIFIED_ROLE_ID = 1371885746415341648
ALLOWED_CHANNEL_ID = 1318298515948048549
HYPERBEAM_LINK = "https://hyperbeam.com/v/wereallinlove"

class HyperbeamCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="hyperbeam", description="Post the server's Hyperbeam watch party link.")
    async def hyperbeam(self, interaction: discord.Interaction):
        # Check role
        if not any(role.id == VERIFIED_ROLE_ID for role in interaction.user.roles):
            return await interaction.response.send_message("You don't have permission to use this command.", ephemeral=True)

        # Check channel
        if interaction.channel.id != ALLOWED_CHANNEL_ID:
            return await interaction.response.send_message("This command can only be used in the watch party channel.", ephemeral=True)

        # Load thumbnail image as a file
        file = discord.File("checkerboard.png", filename="checkerboard.png")

        # Build the embed
        embed = discord.Embed(
            title=f"Join 🎀's Watch Party",
            description=f"{HYPERBEAM_LINK}\n*Click here to join the Hyperbeam session*",
            color=0xFF69B4  # Signature server pink
        )
        embed.set_thumbnail(url="attachment://checkerboard.png")

        await interaction.response.send_message(embed=embed, file=file)

async def setup(bot):
    await bot.add_cog(HyperbeamCommand(bot))
