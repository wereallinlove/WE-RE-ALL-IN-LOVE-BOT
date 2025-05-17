import discord
from discord import app_commands
from discord.ext import commands
import random

LOVELY_IMAGES = [
    "https://media.tenor.com/14udFQfQ7NQAAAAC/pixel-hearts.gif",
    "https://media.tenor.com/yheo1GGu3FwAAAAC/heart.gif",
    "https://media.tenor.com/3N0aUzZ9c38AAAAC/hearts.gif"
]

class Loveletter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="loveletter", description="Send an anonymous love letter to someone")
    @app_commands.describe(user="The person you want to send it to", message="The love letter message")
    async def loveletter(self, interaction: discord.Interaction, user: discord.User, message: str):
        embed = discord.Embed(
            title="💌 Love Letter",
            description=f"*{message}*\n\nTo: {user.mention}",
            color=discord.Color.pink()
        )
        embed.set_image(url=random.choice(LOVELY_IMAGES))
        embed.set_footer(text=f"WE'RE ALL IN LOVE {discord.utils.utcnow().year}")

        channel = self.bot.get_channel(1372782806446506047)
        if channel:
            await channel.send(embed=embed)
            await interaction.response.send_message("Your love letter was sent anonymously! 😍", ephemeral=True)
        else:
            await interaction.response.send_message("Failed to find the love letter channel.", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(Loveletter(bot))
