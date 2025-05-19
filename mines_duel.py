import discord
from discord.ext import commands
from discord import app_commands
import random
import asyncio

class MinesDuel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="minesduel", description="Challenge someone to a Mines duel.")
    @app_commands.describe(user="The user to duel", mines="Number of mines to place (1–24)")
    async def minesduel(self, interaction: discord.Interaction, user: discord.User, mines: int):
        allowed_channel = 1373112868249145485
        allowed_role_id = 1371885746415341648

        if interaction.channel.id != allowed_channel:
            return await interaction.response.send_message("Use this in the correct channel.", ephemeral=True)

        if not any(role.id == allowed_role_id for role in interaction.user.roles):
            return await interaction.response.send_message("You don’t have permission to use this command.", ephemeral=True)

        if user.id == interaction.user.id:
            return await interaction.response.send_message("You can't duel yourself.", ephemeral=True)

        if mines < 1 or mines > 24:
            return await interaction.response.send_message("Choose between 1 and 24 mines.", ephemeral=True)

        challenger = interaction.user
        challenged = user

        class AcceptView(discord.ui.View):
            def __init__(self):
                super().__init__(timeout=3600)

            @discord.ui.button(label="Accept Duel", style=discord.ButtonStyle.success)
            async def accept(self, i: discord.Interaction, button: discord.ui.Button):
                if i.user.id != challenged.id:
                    return await i.response.send_message("Only the challenged user can accept.", ephemeral=True)
                self.stop()
                await start_duel(interaction, challenger, challenged, mines)

            async def on_timeout(self):
                await interaction.followup.send(f"{challenged.mention} didn’t accept in time. Duel cancelled.", ephemeral=False)

        embed = discord.Embed(
            title=f"{challenger.display_name} challenged {challenged.display_name} to a Mines Duel!",
            description=(
                f"{challenged.mention}, you have 1 hour to accept.
"
                f"Each player will try to uncover as many safe tiles as possible with **{mines}** bombs. "
                f"First to hit a bomb loses."
            ),
            color=discord.Color.magenta()
        )
        await interaction.response.send_message(embed=embed, view=AcceptView())

async def setup(bot):
    await bot.add_cog(MinesDuel(bot))
