import discord
from discord.ext import commands
from discord import app_commands
import datetime

class QuoteCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="quote", description="Quote someone and post it in the memory channel.")
    @app_commands.describe(user="Who you're quoting", message="What they said")
    async def quote(self, interaction: discord.Interaction, user: discord.User, message: str):
        quote_channel = self.bot.get_channel(1372918174877614100)
        if not quote_channel:
            await interaction.response.send_message("Couldn't find the quote channel.", ephemeral=True)
            return

        now = discord.utils.utcnow()
        formatted_time = now.strftime("%B %d, %Y at %I:%M %p")

        embed = discord.Embed(
            title=f"Quote from {user.display_name}",
            description=f"“*{message}*”\n\n— {user.mention} ({formatted_time})",
            color=discord.Color.blue()
        )
        embed.set_footer(text="WE'RE ALL IN LOVE")

        await quote_channel.send(embed=embed)
        await interaction.response.send_message("Quote posted successfully.", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(QuoteCommand(bot))
