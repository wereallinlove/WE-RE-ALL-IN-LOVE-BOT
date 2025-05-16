import discord
from discord import app_commands
from datetime import datetime

LOVELETTER_CHANNEL_ID = 1372782806446506047
LOVELETTER_IMAGE_URL = "https://media.tenor.com/Ln9wPaZ0N5sAAAAM/hearts-love.gif"

def setup(bot):
    @bot.tree.command(name="loveletter", description="Send an anonymous love letter to someone")
    @app_commands.describe(user="The person you want to send the letter to", message="The note to send anonymously")
    async def loveletter(interaction: discord.Interaction, user: discord.User, message: str):
        current_year = datetime.now().year
        embed = discord.Embed(
            title="💌 Love Letter",
            description=f"*{message}*\n\nTo: {user.mention}",
            color=discord.Color.from_rgb(255, 80, 160)
        )
        embed.set_image(url=LOVELETTER_IMAGE_URL)
        embed.set_footer(text=f"WE'RE ALL IN LOVE {current_year}")

        channel = bot.get_channel(LOVELETTER_CHANNEL_ID)
        if channel:
            await channel.send(embed=embed)
            await interaction.response.defer(ephemeral=True)
            await interaction.followup.send("Your love letter was sent anonymously. 💌", ephemeral=True)
        else:
            await interaction.response.send_message("Couldn't find the love letter channel.", ephemeral=True)
