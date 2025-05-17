import discord
from discord.ext import commands
from discord import app_commands
import random

class LoveletterCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="loveletter", description="Send an anonymous love letter to someone.")
    @app_commands.describe(user="The person you want to send it to", message="Your anonymous message to them")
    async def loveletter(self, interaction: discord.Interaction, user: discord.User, message: str):
        love_channel = self.bot.get_channel(1372782806446506047)
        if not love_channel:
            await interaction.response.send_message("Love letter channel not found.", ephemeral=True)
            return

        embed = discord.Embed(
            title="💌 Love Letter",
            description=f"*{message}*\n\nTo: {user.mention}",
            color=discord.Color.pink()
        )

        love_gifs = [
            "https://media.tenor.com/14udFQfQ7NQAAAAC/pixel-hearts.gif",
            "https://media.tenor.com/yheo1GGu3FwAAAAC/heart.gif",
            "https://media.tenor.com/3N0aUzZ9c38AAAAC/hearts.gif",
            "https://media.tenor.com/xUa0jz2NS9kAAAAC/pink-love.gif",
            "https://media.tenor.com/_4YgA77ExHEAAAAC/love.gif"
        ]
        embed.set_image(url=random.choice(love_gifs))
        embed.set_footer(text=f"WE'RE ALL IN LOVE {discord.utils.utcnow().year}")

        await love_channel.send(embed=embed)
        await interaction.response.send_message("Your love letter was sent anonymously 💘", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(LoveletterCommand(bot))
