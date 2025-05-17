import discord
from discord import app_commands
from discord.ext import commands

class QuoteCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="quote", description="Quote a message from someone")
    async def quote(self, interaction: discord.Interaction, message: str, user: discord.User):
        embed = discord.Embed(
            title=f"Quote from {user.name}",
            description=f"*{message}*\n\n- ({user.mention})",
            color=discord.Color.blue()
        )
        embed.set_footer(text=f"WE'RE ALL IN LOVE {discord.utils.utcnow().year}")

        channel = self.bot.get_channel(1372918174877614100)
        if channel:
            await channel.send(embed=embed)
            await interaction.response.send_message("Quote shared successfully.", ephemeral=True)
        else:
            await interaction.response.send_message("Couldn't find the quote channel.", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(QuoteCommand(bot))
